import React, { Component } from 'react';
import {Button} from "react-bootstrap";



import axios from 'axios';
import Pdf from "react-to-pdf";
const ref = React.createRef();
class Post extends Component {
    state = {
        persons:[]
    }
    componentDidMount() {
        axios.get(`https://jsonplaceholder.typicode.com/users`)
            .then(res => {
                const persons = res.data;
                this.setState({ persons });
            })
    }




   /* fetchUsersWithAxios = () => {
        this.setState({...this.state, isFetching: true});
        axios.get(USER_SERVICE_URL)
            .then(response => {
                this.setState({data: response.data, isFetching: false})
            })
            .catch(e => {
                console.log(e);
                this.setState({...this.state, isFetching: false});
            });
    };
    fetchUsers = this.fetchUsersWithAxios*/

    render(){
        return(
            <>
                <div className="home-container">
                    <div className="form">

                <ul>
                    {
                        this.state.persons
                            .map(person =>
                                <div className="Post" ref={ref}><h1>{person.name}</h1> <p>{person.username}</p></div>


                            )

                    }
                </ul>
                <Pdf targetRef={ref} filename="HealthCard.pdf">
                    {({ toPdf }) => <Button onClick={toPdf} variant="secondary"   >Capture as PDF</Button>}
                </Pdf>
                </div>
                </div>
            </>
        );
    }
}

export default Post;