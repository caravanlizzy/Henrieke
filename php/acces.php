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

$conn->close();
?>


