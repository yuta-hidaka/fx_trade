import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
// import App from './App';
import * as serviceWorker from './serviceWorker';
import Button from '@material-ui/core/Button';

// ReactDOM.render(<App />, document.getElementById('root'));

function App() {
    return (
        <Button variant="contained" color="primary">
            Hello World
    </Button>
    );
}

ReactDOM.render(<App />, document.querySelector('#app'));
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

