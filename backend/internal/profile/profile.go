package profile

type GradingProfile struct {
	ID        string
	OrgID     string
	StoneType string
	Thresholds map[string]float32
	Version   int
}
