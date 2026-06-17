package device

// Device is a thin stereo + LiDAR capture unit. It runs no inference, so it
// tracks a firmware version rather than a model bundle version.
type Device struct {
	ID              string
	OrgID           string
	Enrolled        bool
	FirmwareVersion string
}
