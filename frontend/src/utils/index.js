import { S3Client } from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";

const s3Client = new S3Client({
  region: "us-east-2",
  credentials: {
    accessKeyId: import.meta.env.VITE_ACCESS_KEY_ID,
    secretAccessKey: import.meta.env.VITE_SECRET_ACCESS_KEY,
  },
});

export const uploadFileToS3 = async (file) => {
  try {
    const upload = new Upload({
      client: s3Client,
      params: {
        Bucket: import.meta.env.REACT_APP_S3_BUCKET_NAME,
        Key: file.name, // File name as the key
        Body: file, // File content
      },
    });

    await upload.done();
    console.log("File uploaded successfully:", file.name);
    return `https://${import.meta.env.REACT_APP_S3_BUCKET_NAME}.s3.${
      import.meta.env.REACT_APP_AWS_REGION
    }.amazonaws.com/${file.name}`;
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export default s3Client;
