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

// Scan is one slab-patch capture. The device produces RGB-D (stereo RGB +
// LiDAR depth); both are stored as object refs. ModelVersion/ProfileVersion
// record which cloud model and grading profile produced the result.
type Scan struct {
	ID             string
	SlabID         string
	RGBRef         string
	DepthRef       string
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
