{{- define "bookshop.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
{{- end }}

{{- define "bookshop.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{- define "bookshop.env" -}}
envFrom:
  - configMapRef:
      name: {{ .Release.Name }}
  - secretRef:
      name: {{ .Values.existingSecret }}
{{- end }}
