// minihelm renders a chart's templates with Go's text/template and the handful
// of Helm functions this chart uses (include, nindent, quote, default, toYaml,
// sha256sum). It is a test stand-in for `helm template`, not a replacement.
//
// Usage: minihelm <chart-dir> <values.json> <release-name>
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"text/template"
)

func toYaml(v any) string {
	var b strings.Builder
	var walk func(v any, indent int)
	walk = func(v any, indent int) {
		pad := strings.Repeat("  ", indent)
		switch t := v.(type) {
		case map[string]any:
			keys := make([]string, 0, len(t))
			for k := range t {
				keys = append(keys, k)
			}
			sort.Strings(keys)
			for _, k := range keys {
				if m, ok := t[k].(map[string]any); ok {
					b.WriteString(pad + k + ":\n")
					walk(m, indent+1)
				} else {
					b.WriteString(fmt.Sprintf("%s%s: %v\n", pad, k, t[k]))
				}
			}
		default:
			b.WriteString(fmt.Sprintf("%s%v\n", pad, t))
		}
	}
	walk(v, 0)
	return strings.TrimSuffix(b.String(), "\n")
}

func main() {
	chart, valuesPath, release := os.Args[1], os.Args[2], os.Args[3]
	raw, _ := os.ReadFile(valuesPath)
	var values map[string]any
	if err := json.Unmarshal(raw, &values); err != nil {
		panic(err)
	}
	var meta map[string]any
	metaRaw, _ := os.ReadFile(filepath.Join(chart, "Chart.json"))
	if err := json.Unmarshal(metaRaw, &meta); err != nil {
		panic(err)
	}
	ctx := map[string]any{
		"Values":   values,
		"Release":  map[string]any{"Name": release},
		"Chart":    map[string]any{"Name": meta["name"], "Version": meta["version"], "AppVersion": meta["appVersion"]},
		"Template": map[string]any{"BasePath": "catalog/templates"},
	}
	root := template.New("root").Option("missingkey=error")
	sources := map[string]string{}
	funcs := template.FuncMap{
		"nindent": func(n int, s string) string {
			pad := strings.Repeat(" ", n)
			return "\n" + pad + strings.ReplaceAll(s, "\n", "\n"+pad)
		},
		"quote": func(v any) string { return fmt.Sprintf("%q", fmt.Sprint(v)) },
		"default": func(d any, v any) any {
			if v == nil || v == "" {
				return d
			}
			return v
		},
		"toYaml":    toYaml,
		"sha256sum": func(s string) string { h := sha256.Sum256([]byte(s)); return hex.EncodeToString(h[:]) },
		"print":     fmt.Sprint,
		"include": func(name string, data any) (string, error) {
			var buf bytes.Buffer
			err := root.ExecuteTemplate(&buf, name, data)
			return buf.String(), err
		},
	}
	root.Funcs(funcs)
	files, _ := filepath.Glob(filepath.Join(chart, "templates", "*"))
	sort.Strings(files)
	for _, f := range files {
		src, _ := os.ReadFile(f)
		name := "catalog/templates/" + filepath.Base(f)
		sources[name] = string(src)
		if _, err := root.New(name).Parse(string(src)); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	}
	for _, f := range files {
		name := "catalog/templates/" + filepath.Base(f)
		if strings.HasPrefix(filepath.Base(f), "_") {
			continue
		}
		var buf bytes.Buffer
		if err := root.ExecuteTemplate(&buf, name, ctx); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		fmt.Printf("---\n# Source: %s\n%s\n", name, strings.TrimSpace(buf.String()))
	}
}
