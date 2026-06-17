package registry

// ModelImage is a versioned inference model served in-cluster (deployed as a
// container image). Cloud inference replaces the old signed-OTA bundle model,
// so there is no on-device bundle or signature.
type ModelImage struct {
	Version  string
	ImageRef string // container image reference deployed to the GPU node pool
	Metrics  map[string]float64
}
