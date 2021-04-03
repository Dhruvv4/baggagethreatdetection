import React from "react";
import "./ResultImage.css";

export const ResultImage = ({imgUrl}) => {
  return (
    <div>
      <h1>Result</h1>
      <img className="detected__image" src={imgUrl} alt="" />
    </div>
  );
};

export default ResultImage;
