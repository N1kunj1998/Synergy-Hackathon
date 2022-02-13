import React, { useState } from 'react'
import './homeStyles.css'
import { WebcamCapture} from '../Webcam/Webcam'


const Home = () => {
    


    return (
        <div className="home-container">
            <div className="container">
                <div className="text">
                    <h1>Kindly take a picture of Your Aadhar card !</h1>
                    <form className="form">
                        <WebcamCapture/>


                    </form>
                </div>
            </div>
        </div>
    )
}
export default Home
