import { useEffect, useState } from 'react';
import Button from '@mui/material/Button';

export default function TextBlob(props){
    return (
        <div>
            <Button variant="text">{props.text}</Button>
        </div>
    )
}
