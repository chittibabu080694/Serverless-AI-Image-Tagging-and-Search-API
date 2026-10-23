provider "aws" {
  region = "ap-south-1"
}

# S3 Bucket for Images
resource "aws_s3_bucket" "image_bucket" {
  bucket        = "ai-image-tagging-bucket-94"
  force_destroy = true
}

# DynamoDB Table for Image Metadata
resource "aws_dynamodb_table" "image_metadata" {
  name         = "ImageMetadata"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ImageKey"

  attribute {
    name = "ImageKey"
    type = "S/W" # String type
  }
}
