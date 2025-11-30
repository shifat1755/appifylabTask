import { getSignedS3Url } from "../service/media"


export async function fileUpload(file: File) {
    const { presigned_url, file_path } = await getSignedS3Url(file.name, file.type);

    await fetch(presigned_url, {
        method: "PUT",
        headers: {
            'Content-Type': file.type,
        },
        body: file,
    }).catch(err => {
        throw new Error("File upload failed. Please try again later.", err);
    });
    return file_path;
}