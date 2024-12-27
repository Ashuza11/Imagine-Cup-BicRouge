import { BlobServiceClient, StorageSharedKeyCredential } from "@azure/storage-blob";

const blobServiceClient = new BlobServiceClient(
  `https://${import.meta.env.VITE_AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net`,
  new StorageSharedKeyCredential(
    import.meta.env.VITE_AZURE_STORAGE_ACCOUNT_NAME,
    import.meta.env.VITE_AZURE_STORAGE_ACCOUNT_KEY
  )
);

export const uploadFileToAzure = async (file) => {
  try {
    const containerClient = blobServiceClient.getContainerClient(import.meta.env.VITE_AZURE_CONTAINER_NAME);
    const blockBlobClient = containerClient.getBlockBlobClient(file.name);

    await blockBlobClient.uploadBrowserData(file);
    console.log("File uploaded successfully:", file.name);
    return blockBlobClient.url;
  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};

export default blobServiceClient;