import api from "./axiosApi";

export function getSignedS3Url(fileName: string, fileType: string) {
    return api.post("/media/s3/presigned-url", {
        file_name: fileName,
        file_type: fileType,
    })
        .then(res => res.data)
        .catch(err => {
            throw new Error("Failed to get signed S3 URL. Please try again later.", err);
        });
}
