// function to create a cloud storage bucket
func createBucket(w io.Writer, projectID, bucketName string) (*storage.Bucket, error) {
	// bucketName := "test-go-bucket123"
	ctx := context.Background()
	client, err := storage.NewClient(ctx)
	if err != nil {
		return nil, fmt.Errorf("storage.NewClient: %v", err)
	}
	defer client.Close()

	ctx, cancel := context.WithTimeout(ctx, time.Second*10)
	defer cancel()

	bucket := client.Bucket(bucketName)
	if err := bucket.Create(ctx, projectID, nil); err != nil {
		return nil, fmt.Errorf("Bucket(%q).Create: %v", bucketName, err)
	}
	fmt.Fprintf(w, "Bucket %v created\n", bucketName)
	return bucket, nil
}
// https://github.com/GoogleCloudPlatform/golang-samples/blob/main/storage/buckets/create_bucket.go