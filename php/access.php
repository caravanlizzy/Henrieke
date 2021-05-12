<?php

// require "dbconnecter.php";
require "game.php";
require "response.php";
require "login.php"; //this file  is not part of the .git repository

$servername = "localhost";
$username = $name;
$password = $pw;
$db = $dbName;


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



function handleGet(){ //handle get requests
    $noIdCheckTasks = array("createGame", "joinGame");
    $task = $_GET["task"];
    if(!in_array($task, $noIdCheckTasks)){
        if(!checkId()) { 
            return;
        }
    }
    call_user_func($task);
}

function checkId() { //verify player identity
    global $conn;
    $playerId = $_GET["playerId"];
    $gameId = $_GET["gameId"];
    $pw = $_GET["pw"];
    $game = new Game($conn, $gameId);
    $approved = $game->checkId($playerId, $pw);
    return $approved;
}

function playCard(){ //play a card
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];
    $playerId = $_GET["playerId"];
    $card = $_GET["card"];
    $game = new Game($conn, $gameId);
    $result = $game->playCard($playerId, $card);
    $res->sendPlayCard($result);
}

function startGame() { //start game
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $game->startGame();
    $res->sendGameState("running");
}

function createGame() { //create a new game
    global $conn;
    $game = new Game($conn);
    $gameId = $game->createGame();
    echo $gameId; 
}

function joinGame() { //player joins a game
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $nick = $_GET["nick"];
    $playerInfo = $game->addPlayer($nick); 
    $res->sendPlayerInfo($playerInfo);
}

function addComputer() { //add a bot
    global $conn;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $playerId = $game->addPlayer("Computer");
    // need to initialize the bot here
}

function removeGame() {
    global $conn;
    $gameId = $_GET["gameId"];
    $game = new Game($conn, $gameId);
    $game->dbConnecter->removeGame();
}


// function endRound() { //check whether all acrds are played
//     global $conn;
//     global $res;
//     $gameId = $_GET["gameId"];  
//     $game = new Game($conn, $gameId);
//     $complete = $game->checkMoveComplete();
//     $res->sendMoveComplete($complete);
// }

function getGame() {
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $gameComplete = $game->getGame();
    $res->sendGame($gameComplete);
}


function endRound() { // do the end of round calculations
    global $conn;
    global $res;
    $gameId = $_GET["gameId"];  
    $game = new Game($conn, $gameId);
    $newDecksNCrowns = $game->endRound();
    $res->sendRoundEnd($newDecksNCrowns);
}

$conn->close();
?>


