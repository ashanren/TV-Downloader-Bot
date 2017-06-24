import React from 'react';
import { Button, FormControl } from 'react-bootstrap'

class Body extends React.Component {
	constructor(props)
	{
		super(props);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.button = <FormControl type="submit" value="Download" />;
		this.http = null;
	}
	
	handleSubmit(event)
	{
		event.preventDefault();
		this.http = new XMLHttpRequest();
		this.http.open("POST", "http://localhost:5000", true);
		this.http.onreadystate = () =>
		{
			if ( this.http.readyState == 4 && this.http.status == 200)
			{
				console.log("Sup");
				alert("Console.log is not the correct printing for the frontend");
			}
		};
		this.http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		this.http.send("Post message");
	}
	render(){

		return(
			<div>
				<h1>Testing Button</h1>
				<form onSubmit={this.handleSubmit}>
					{this.button}
				</form>
			</div>
		)
			
	}


}

export default Body
