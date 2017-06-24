import React from 'react';
import ReactDOM from 'react-dom';

import Body from './components/body.component'

class App extends React.Component {

	render () {
		return (
			<Body />
		);
			
	}

}

ReactDOM.render(
	  <App />,
	  document.getElementById('content')
);
