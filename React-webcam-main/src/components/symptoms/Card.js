import React from 'react'
import './Card.css'
function Card({title,imageUrl,body}){
    const issymp=()=> {
        console.log(title)
    }
    return(
        <div className='card-container'>

            <div className='image-container'>
                <img src={imageUrl} alt='symptons'/>
            </div>
            <div className='card-title'>
                <h2>{title}</h2>
            </div>
            <div className='card-body'>
                <h3>{body}</h3>
            </div>
            <div className='btn'>
                <button onclick={issymp()}>I have it!</button>
            </div>

        </div>
    )
}
export default Card;