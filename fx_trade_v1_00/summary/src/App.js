// import React, { Component } from "react";
// import NavBar from "./components/NavBar";

// class App extends Component {
//   render() {
//     return (
//       <div>
//         <NavBar />
//       </div>
//     );
//   }
// }

// export default App;

// import React from "react";
import React, { Component } from "react";

// import logo from "./logo.svg";
import "./App.css";
// import Button from "@material-ui/core/Button";
import { Paper, Typography, TextField, Button } from "@material-ui/core";

class App extends Component {
  state = {
    exercises: [],
    title: ""
  };
  handleChange = ({ target: { name, value } }) =>
    this.setState({ [name]: value });
  render() {
    const { title } = this.state;
    return (
      <Paper>
        <Typography
          variant="subtitle1"
          align="center"
          className="MuiTypography-subtitle1"
          gutterBottom
        >
          Exercises
        </Typography>
        <form>
          <TextField
            name="title"
            label="Exercise"
            value={title}
            onChange={this.handleChange}
            margin="normal"
            align="center"
          />
          <Button type="submit" color="primary" variant="contained">
            作成
          </Button>
        </form>
      </Paper>
    );
    // render() {
    //   return (

    //   );
  }
  // render() {
  //   return <h1>Exercises</h1>;

  // }
}
export default App;

// function App() {
//   //  render() {
//      return (
//         <Typography variant='h1' align='center' gutterBottom>
//                   Exercises
//         </Typography>)
//         // }
// }

// class mainView extends React.Component{

//    render() {
//      return (
//         <Typography variant='display1' align='center' gutterBottom>
//                   Exercises
//         </Typography>)}
// }

// export default App;

// function Square(props) {
//   return (
//     <button className="square" onClick={props.onClick}>
//       {props.value}
//     </button>
//   );
// }

// function calculateWinner(squares) {
//   console.log(squares);
//   const lines = [
//     [0, 1, 2],
//     [3, 4, 5],
//     [6, 7, 8],
//     [0, 3, 6],
//     [1, 4, 7],
//     [2, 5, 8],
//     [0, 4, 8],
//     [2, 4, 6]
//   ];
//   for (let i = 0; i < lines.length; i++) {
//     const [a, b, c] = lines[i];
//     if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
//       console.log(squares[a]);
//       return squares[a];
//     }
//   }
//   return null;
// }
// // class Square extends React.Component {
// //   // 最初はSquareに値を個別に書き込んでいた
// //   // 次にしたことは、スクエアコンポーネントを下位てonClickで下記を呼び出し、呼び出し元に値を再度渡した

// //   // prop引数ー呼び出し先の何か
// //   // state内部で保持する値？

// //   // constructor(props) {
// //   //   // クラスコンポーネントではすべてのコンストラクタをsuper(props)から呼び出し
// //   //   super(props);
// //   //   this.state = {
// //   //     value: null
// //   //     // a: null
// //   //   };
// //   // }

// //   render() {

// //     // return (
// //     //   <button
// //     //     className="square"
// //     //     onClick={() => {
// //     //       // this.setState({ value: "✖" });
// //     //       alert("clicked!--squre");
// //     //       this.props.onClick();
// //     //       alert("clicked!--squre--end");
// //     //     }}
// //     //   >
// //     //     {this.props.value}
// //     //     {/* {this.state.value} */}
// //     //   </button>
// //     // );
// //   }
// // }

// // /:」class Board extends React.Component {
// //   renderSquare(i) {
// //     return <Square value={i} />;
// //   }
// // }
// class Board extends React.Component {
//   // constructor(props) {
//   //   super(props);
//   //   this.state = {
//   //     squares: Array(9).fill(null),
//   //     xIsNext: true
//   //   };
//   // }

//   // handleClick(i) {
//   //   // alert(!this.state.xIsNext);
//   //   const squares = this.state.squares.slice();

//   //   if (calculateWinner(squares) || squares[i]) {
//   //     return;
//   //   }

//   //   squares[i] = this.state.xIsNext ? "✖" : "〇";
//   //   this.setState({
//   //     squares: squares,
//   //     xIsNext: !this.state.xIsNext
//   //   });
//   // }

//   renderSquare(i) {
//     // console.log(this.state.squares);
//     // return <Square value={i} />;
//     return (
//       <Square
//         // value={this.state.squares[i]}
//         value={this.props.squares[i]}
//         // onClick={() => this.handleClick(i)}
//         onClick={() => this.props.onClick(i)}
//       />
//     );
//   }

//   render() {
//     // const status = "Next player: X";
//     // const status = "Next player: " + (this.state.xIsNext ? "X" : "O");
//     // const winner = calculateWinner(this.state.squares);

//     // let status;
//     // if (winner) {
//     //   status = "Winner: " + winner;
//     // } else {
//     //   status = "Nexr player: " + (this.state.xIsNext ? "✖" : "〇");
//     // }

//     return (
//       <div>
//         {/* <div className="status">{status}</div> */}
//         <div className="board-row">
//           {this.renderSquare(0)}
//           {this.renderSquare(1)}
//           {this.renderSquare(2)}
//         </div>
//         <div className="board-row">
//           {this.renderSquare(3)}
//           {this.renderSquare(4)}
//           {this.renderSquare(5)}
//         </div>
//         <div className="board-row">
//           {this.renderSquare(6)}
//           {this.renderSquare(7)}
//           {this.renderSquare(8)}
//         </div>
//       </div>
//     );
//   }
// }

// class Game extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       history: [
//         {
//           squares: Array(9).fill(null)
//         }
//       ],
//       xIsNext: true,
//       stepNumber: 0
//     };
//   }

//   handleClick(i) {
//     // alert(!this.state.xIsNext);
//     const history = this.state.history.slice(0, this.state.stepNumber + 1);
//     const current = history[history.length - 1];
//     const squares = current.squares.slice();
//     // const squares = this.state.squares.slice();

//     if (calculateWinner(squares) || squares[i]) {
//       return;
//     }

//     squares[i] = this.state.xIsNext ? "✖" : "〇";

//     this.setState({
//       history: history.concat([
//         {
//           squares: squares
//         }
//       ]),
//       xIsNext: !this.state.xIsNext,
//       stepNumber: history.length
//     });

//     // this.setState({
//     //   squares: squares,
//     //   xIsNext: !this.state.xIsNext
//     // });
//   }

//   jumpTo(step) {
//     this.setState({
//       stepNumber: step,
//       xIsNext: step % 2 === 0
//     });
//   }

//   render() {
//     const history = this.state.history;
//     const current = history[this.state.stepNumber];
//     const winner = calculateWinner(current.squares);
//     let status;
//     const moves = history.map((step, move) => {
//       const desc = move ? "go to move #" + move : "Go to start";
//       return (
//         <li key={move}>
//           <button onClick={() => this.jumpTo(move)}>{desc}</button>
//         </li>
//       );
//     });

//     if (winner) {
//       status = "Winner: " + winner;
//     } else {
//       status = "Next player: " + (this.state.xIsNext ? "✖" : "〇");
//     }
//     return (
//       <div className="game">
//         <div className="game-board">
//           <Board squares={current.squares} onClick={i => this.handleClick(i)} />
//         </div>
//         <div className="game-info">
//           <div>{status}</div>
//           <ol>{moves}</ol>
//         </div>
//       </div>
//     );
//   }
// }

// export default Game;
