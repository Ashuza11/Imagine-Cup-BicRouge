import { useState } from "react";
import { Upload } from "@aws-sdk/lib-storage";
import s3Client from "../utils";
import { ClipLoader } from "react-spinners";

const FileUpload = ({onSuccess, setSyllabus_url}) => {
  const [file, setFile] = useState(null);
  const [upladSuccess, setUploadSuccess] = useState("");
  const [uploadError, setUploadError] = useState("");
  const [uploadLoading, setUploadLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    setUploadError('')
    setUploadSuccess('')

    try {
      setUploadLoading("Uploading...");
      const upload = new Upload({
        client: s3Client,
        params: {
          Bucket: "recordingsbuclets",
          Key: file.name,
          Body: file,
        },
      });

      const res = await upload.done();
      onSuccess(res.Location)
      setUploadSuccess("Syllabus uploaded successfully!");
      setUploadError('')
    } catch (err) {
      console.error("Syllabus upload failed:", err);
      setUploadSuccess('')
      setUploadError("Upload failed.");
    } finally {
      setUploadLoading(false);
    }
  };

  return (
    <div className="w-full mt-2 flex flex-col gap-1">
      <p>Syllabus</p>
      <div className="w-full flex items-center justify-between h-12">
        <input type="file" onChange={handleFileChange} />
        <button type="button" onClick={handleFileUpload} className=" px-4 border py-2 rounded">
          Upload
        </button>
      </div>
      {uploadLoading && <ClipLoader size={20} className=" h-8 w-8"/>}
      <p className=" text-green-600">{upladSuccess}</p>
      <p className=" text-red-500">{uploadError}</p>
    </div>
  );
};

export default FileUpload;
