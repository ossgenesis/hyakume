package registry

type ModelBundle struct {
	Version   string
	Signature []byte
	Metrics   map[string]float64
}
