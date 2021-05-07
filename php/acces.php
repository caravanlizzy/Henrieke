<?php

// require "dbconnecter.php";
require "game.php";
require "response.php";

$servername = "localhost";
$username = "*********";
$password = "*********";
$db = "********";


// Create connection
$conn = mysqli_connect($servername, $username, $password, $db);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$res = new Response();

if ($_SERVER["REQUEST_METHOD"] == "GET"){
    handleGet();
  }elseif ($_SERVER["REQUEST_METHOD"] == "POST"){
    handlePost();
}



function handleGet(){
    $noIdCheckTasks = array("createGame", "joinGame");
    $task = $_GET["task"];
    if(!in_array($task, $noIdCheckTasks)){
        if(!checkId()) {
            return;
        }
    }
    call_user_func($task);
}

function checkId() {
    global $conn;
    $playerId = $_GET["playerId"];
    $gameId = $_GET["gameId"];
    $pw = $_GET["pw"];
    $game = new Game($conn, $gameId);
    $approved = $game->checkId($playerId, $pw);
    return $approved;
}

function playCard(){
    global $conn;
    $gameId = $_GET["gameId"];
    $playerId = $_GET["playerId"];
    $card = $_GET["card"];
    $game = new Game($conn, $gameId);
    $result = $game->playCard($playerId, $card);
    echo $result;
}

function startGame() {
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $game->startGame();
    $res->sendGameState("running");
}

function createGame() {
    global $conn;
    $game = new Game($conn);
    $gameId = $game->createGame();
    echo $gameId; 
}

function joinGame() {
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $nick = $_GET["nick"];
    $playerInfo = $game->addPlayer($nick); 
    $res->sendPlayerInfo($playerInfo);
}

function addComputer() {
    global $conn;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $playerId = $game->addPlayer("Computer");
    // need to initialize the bot here
}


function allCardsPlaced() {
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $complete = $game->checkMoveComplete();
    $res->sendMoveComplete($complete);
}

function endRound() {
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $newDecksNCrowns = $game->endRound();
    $res->sendRoundEnd($newDecksNCrowns);
}


// function updateGame() {
//     global $conn;
//     $gameId = $_GET["gameId"];  
//     $game = new Game($conn, $gameId);
// }

// function createGame() {
//     global $conn;
//     $gameId = $_GET["gameId"];
//     $playerId = $_GET["playerId"];
//     $newGame = new Game($conn, $gameId);
//     return $newGame;
// }


// $gameId = 1;
// $game = new Game($conn, $gameId);
// $game->dbConnecter->resetMove();
// $game->deleteGame();
// $game->createGame();
// $game->startGame();
// $game->addPlayer("player1");
// $game->addPlayer("player2");
// $game->addPlayer("player3");
// $game->addPlayer("player4");
// $game->playCard(1,5);
// $game->playCard(2,7);
// $game->playCard(3,2);
// $game->playCard(4,9);
// $game->playCard(1,0);
// $game->playCard(2,0);
// $game->playCard(3,0);
// $game->playCard(4,2);



// if ($_SERVER["REQUEST_METHOD"] == "GET"){
//     handleGet();
//   }elseif ($_SERVER["REQUEST_METHOD"] == "POST"){
//     handlePost();
// }


// function handleGet(){
//     $task = $_GET["task"];
//     // $data = $_GET["data"];
//         switch ($task) {
//         case "getPlayers":
//             get_players();
//             break;
//         case "getTourneys":
//             get_tourneys();
//             break;
//         default:
//             echo "Error: Get request could not be handled.";
//     };
// }


$conn->close();
?>


