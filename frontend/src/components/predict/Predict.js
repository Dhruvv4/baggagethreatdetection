import React, {useState, useRef} from "react";
import ResultImage from "../result/ResultImage";
import axios from "axios";
import {CSVLink} from "react-csv";

export const Predict = () => {
  const onSubmit = () => {
    const imageFile = document.getElementById("imageFile").files[0];
    const xmlFile = document.getElementById("xmlFile").files[0];
    if (!imageFile || !xmlFile) {
      return null;
    }
    const formData = new FormData();
    formData.append("imgFile", imageFile);
    formData.append("xmlFile", xmlFile);

    const url = "http://localhost:5000/predict";
    axios.post(url, formData, {responseType: "blob"}).then(
      (res) => {
        const imgUrl = URL.createObjectURL(res.data);
        setImage(imgUrl);
        setCanShow(true);
      },
      (error) => {
        console.log(error);
      }
    );
  };

  const onImageFileEvent = (e) => {
    if (e?.target?.files?.length > 0) {
      document.getElementById("imageInputText").innerHTML =
        e.target.files[0].name;
    }
  };

  const onXMLFileEvent = (e) => {
    if (e?.target?.files?.length > 0) {
      document.getElementById("xmlInputText").innerHTML =
        e.target.files[0].name;
    }
  };

  const exportData = (e) => {
    const url = "http://localhost:5000/export";
    axios.get(url).then((res) => {
      setCsvData(res.data);
      csvLinkRef.current.link.click();
    });
  };

  const [image, setImage] = useState("");
  const [canShow, setCanShow] = useState(false);
  const [csvData, setCsvData] = useState("");
  const csvLinkRef = useRef();

  return (
    <div className="container d-flex justify-content-center">
      <div className="login__section">
        <h1>Upload Files</h1>
        <form>
          <div className="form-group">
            <div className="custom-file">
              <input
                type="file"
                className="custom-file-input"
                id="imageFile"
                accept=".jpg,.jpeg"
                onChange={onImageFileEvent}
              />
              <label
                id="imageInputText"
                className="custom-file-label"
                htmlFor="customFile"
              >
                Choose Image file
              </label>
            </div>
          </div>
          <div className="form-group">
            <div className="custom-file">
              <input
                type="file"
                className="custom-file-input"
                id="xmlFile"
                accept=".xml"
                onChange={onXMLFileEvent}
              />
              <label
                id="xmlInputText"
                className="custom-file-label"
                htmlFor="customFile"
              >
                Choose XML file
              </label>
            </div>
          </div>
          <div className="d-flex justify-content-between">
            <button
              type="button"
              className="btn btn-info btn-sm"
              onClick={onSubmit}
            >
              Detect
            </button>
            <button
              type="button"
              className="btn btn-sm btn-info"
              onClick={exportData}
            >
              Export Data
            </button>
          </div>
        </form>
      </div>
      <div className={canShow ? "m-5" : ""}></div>
      <div className="result__section">
        {canShow && <ResultImage imgUrl={image} />}
      </div>
      <CSVLink
        id="csvLink"
        filename={"export.csv"}
        target="_self"
        data={csvData}
        ref={csvLinkRef}
      ></CSVLink>
    </div>
  );
};

export default Predict;
