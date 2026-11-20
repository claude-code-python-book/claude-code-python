{{- define "catalog.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}
{{- end }}

{{- define "catalog.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}

{{- define "catalog.env" -}}
envFrom:
  - configMapRef:
      name: {{ .Release.Name }}
  - secretRef:
      name: {{ .Values.existingSecret }}
{{- end }}
