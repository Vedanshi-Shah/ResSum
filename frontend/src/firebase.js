import {initializeApp} from "firebase/app";
import {getStorage} from "firebase/storage";
import { getFirestore } from "firebase/firestore";

// const { applicationDefault, cert } = require('firebase-admin/app');
// const { getFirestore, Timestamp, FieldValue } = require('firebase-admin/firestore');

const app=initializeApp({
    apiKey: "AIzaSyBwS4L-3ZMgyfFZJCUznaqxz6hKmvlucvQ",
    authDomain: "text-summarizer-storage.firebaseapp.com",
    projectId: "text-summarizer-storage",
    storageBucket: "text-summarizer-storage.appspot.com",
    messagingSenderId: "405194403681",
    appId: "1:405194403681:web:96d14a6660cfe9724ddf20"
});
const storage=getStorage(app);
const db=getFirestore();
export {storage, db};
