import React, { useState } from 'react';
import './homeStyles.css';
import Card from './Card'



const Symptoms = () => {



    return (
        <div className="home-container">
            <h1 ><b>SYMPTOMS</b></h1>
            <div className="container">

                    <Card
                        title='Cold'
                        imageUrl='https://en.pimg.jp/047/105/602/1/47105602.jpg'
                        body='Area:FullBody'

                    />
                    <Card
                        title='Migrain'
                        imageUrl='https://ichef.bbci.co.uk/news/776/cpsprodpb/26DE/production/_99005990_542093304.jpg'
                        body='Area:Head'

                    />
                    <Card
                        title='Vomiting'
                        imageUrl='https://thumbs.dreamstime.com/b/sick-girl-vomiting-cartoon-illustration-93219926.jpg'
                        body='Area:Digestive System'

                    />
                <Card
                    title='Swollen Glands'
                    imageUrl='https://media.istockphoto.com/vectors/the-girl-suffers-from-a-sore-throat-the-woman-fell-ill-with-angina-a-vector-id1304179780?k=20&m=1304179780&s=612x612&w=0&h=PJGXpY1rhUwJbtRO8s1zHGOCGp4_5LsL6clKSOWflFs='
                    body='Area:Epiglotis'

                />
                <Card
                    title='Nausea'
                    imageUrl='https://previews.123rf.com/images/kakigori/kakigori1806/kakigori180600021/104567300-bambina-sveglia-malata-di-nausea-con-espressione-del-viso-verde-sensazione-di-malessere.jpg'
                    body='Area:Nose'

                />
                <Card
                    title='Rash'
                    imageUrl='https://us.123rf.com/450wm/goodstocker/goodstocker1810/goodstocker181000436/110605726-cartoon-young-man-with-red-spots-on-his-face-cartoon-design-icon-colorfull-flat-vector-illustration-.jpg?ver=6'
                    body='Area:Skin'

                />


            </div>
        </div>
    )
}
export default Symptoms;
