import { useEffect, useState } from 'react';
import {storage, db} from "./firebase";
import { TextField } from '@mui/material';
import { styled } from '@mui/material/styles';
// import logo from './logo.svg';
import './App.css';
import {getDownloadURL, ref,uploadBytesResumable} from "firebase/storage";
import "./styles.css";
// import { ReactUpload } from 'react-upload-box'
import { collection, addDoc } from "firebase/firestore"; 
import { LinearProgress } from "@mui/material";
import Button from '@mui/material/Button';

function TextBlob(props){
  return (
      <div>
          <Button variant="text">{props.text}</Button>
      </div>
  )
}

function App() {
  const type = 'pdf'
  const [fileLink, setFileLink] = useState('');
  const [file,setFile]=useState('');
  const [percent,setPercent]=useState(0);
  const [switchDone, setSwitchDone] = useState(0);
  const [summary, setSummary] = useState();
  const [posts, setPosts] = useState({'summary':"Summary will appear here shortly..."});
  const [blobs, setBlobs] = useState([]);

  function upload(event){
    setFile(event.target.files[0]);
    // setUpload(false);
  }

  const downloadTxtFile = () => {
    const element = document.createElement("a");
    const file = new Blob([posts.summary], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = "myFile.txt";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }

  const fetchData = async () => {
    var request = new Request(`http://localhost:8000/extract/${file.name}`);
    const response = await fetch(request);
    const data = await response.json();
    console.log(data.summary);
    console.log("Here");
    console.log(posts);
    console.log("--------");
    setPosts({
      ...posts,
      summary: data.summary
    });
  };

  const fetchBlobs = async () => {
    console.log("In blobs");
    var request = new Request(`http://localhost:8000/keywords/${file.name}`);
    const response = await fetch(request);
    const data = await response.json();
    console.log(data.blobs);
    console.log("Here");
    console.log("--------");
    setBlobs(data.blobs);
  };

  // console.log(blobs);

  // function blobList() {
  //   // console.log("Here");
  //   // console.log(blobs);
  //   return blobs.map((blob) => {
  //     console.log("Here2");
  //     return (
  //       <BootstrapButton variant="text">{blob.charAt(0).toUpperCase() + blob.slice(1)}</BootstrapButton>
  //     );
  //   });
  // }

  const BootstrapButton = styled(Button)({
    boxShadow: 'none',
    textTransform: 'none',
    fontSize: 16,
    padding: '6px 12px',
    border: '1px solid',
    marginTop: '1px',
    marginBottom: '1px',
    marginLeft: '2px',
    marginRight: '2px',
    lineHeight: 1.5,
    // backgroundColor: '#0063cc',
    // borderColor: '#0063cc',
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    // '&:hover': {
    //   backgroundColor: '#0069d9',
    //   borderColor: '#0062cc',
    //   boxShadow: 'none',
    // },
    // '&:active': {
    //   boxShadow: 'none',
    //   backgroundColor: '#0062cc',
    //   borderColor: '#005cbf',
    // },
    // '&:focus': {
    //   boxShadow: '0 0 0 0.2rem rgba(0,123,255,.5)',
    // },
  });

  // console.log(posts.summary);

  // useEffect(() => {
  //   fetchData();
  // }, [switchDone]);

  function handleUpload(){
    if(!file){
      alert("Please choose a file!");
    }
    console.log("I'm clicked");
    setBlobs([])
    const storageRef=ref(storage,`/files/${file.name}`);
    const uploadTask=uploadBytesResumable(storageRef,file);
    uploadTask.on(
      "state_changed",
      (snapshot)=>{
        const percent=Math.round(
          (snapshot.bytesTransferred/snapshot.totalBytes)*100
        );
        setPercent(percent);
      },
      (err)=>console.log(err),
      ()=>{
        getDownloadURL(uploadTask.snapshot.ref).then((url)=>{
          console.log(url);
          setFileLink(url);
          console.log(file.name);
          const docRef = async () => {await addDoc(collection(db, "users"), {
            file_name: file.name,
            file_url: url
          })};
          docRef();
          url = encodeURI(url);
          fetchBlobs();
          fetchData();
          setPercent(0);
        });
      }
    );
  };
  if (!fileLink){
    return (
      <div className="App">
        <header>
          <h1>ResSum</h1>
        </header>
        <div>
          <LinearProgress id="progress-bar" variant="determinate" value={percent} />
          <div class="io">
            <input type="file" accept="application/pdf" onChange={upload}/>
            <button onClick={handleUpload}>Upload</button>
          </div>
        </div>
      </div>
    );
  } else{
    return (
      <div className="App">
        <header>
          <h1>ResSum</h1>
        </header>
        <div>
          <div id="summary">
            <LinearProgress id="progress-bar" variant="determinate" value={percent} />
            <div class="io">
              <input type="file" accept="application/pdf" onChange={upload}/>
              <button onClick={handleUpload}>Upload</button>
              <button onClick={downloadTxtFile}>Download</button>
            </div>
            {/* <div>
              {blobList()}
            </div> */}
            <div class="text-area">
              <TextField fullWidth id="filled-basic" label="Summary" value={posts.summary} variant="filled" inputProps={{ readOnly: true,}} multiline/>
            </div>
          </div>
          <embed
            id="viewer" 
            src={fileLink}
            type="application/pdf"
            height={800}
            width={500}
          />
        </div>
      </div>
    );
  }
}

export default App;
