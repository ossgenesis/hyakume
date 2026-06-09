package scan

import "time"

type Slab struct {
	ID        string
	SessionID string
	Label     string
	StoneType string
	Grade     string
	CreatedAt time.Time
}

type Scan struct {
	ID             string
	SlabID         string
	ImagesRef      string
	NormalsRef     string
	ModelVersion   string
	ProfileVersion string
	CreatedAt      time.Time
}

type Defect struct {
	ID         string
	ScanID     string
	Type       string
	MaskRef    string
	Confidence float32
}
