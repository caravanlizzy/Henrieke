<?php
require 'dbconnecter.php';
// require 'response.php';

class Game{
    function __construct($conn, $gameId = 0) {
        $this->dbConnecter = new DbConnecter($conn, $gameId);
        $this->gameId = $gameId;
        // print_r($gameId);
    }

    function setGameId($id) {
        $this->gameId = $id;
    }

    function createGame() {
        //host has to be checked
        $gameId = $this->dbConnecter->getHighestGameId() + 1;
        $this->gameId = $this->dbConnecter->createGame($gameId);
        return $gameId;
    }

    function startGame() {
        $this->dbConnecter->setGameState("running");
    }

    function endGame() {
        $this->dbConnecter->setGameState("idle");
    }

    function deleteGame() {
        $this->dbConnecter->deleteAllPlayers();
        $this->dbConnecter->deleteMove();
        $this->dbConnecter->deleteGame();
    }

    function endRound() {
        $result = $this->getRoundResult();
        $decks = $this->updateDecks($result);
        $crowns = $this->getCrowns();
        // $this->response->setDecks($decks);
        // $this->response->setCrowns($crowns);
        $updatedCrown = $this->updateCrowns($result);
        if($this->checkWin($updatedCrown)) {
            $this->endGame();
        } else{
            $this->nextRound();
        }
        $newCrowns =  $this->getCrowns();
        $complete = array($decks, $newCrowns);
        return $complete;
    }

    function getCrowns() {
        $playerIds = $this->dbConnecter->getPlayerIds();
        $crowns = array();
        for($i = 0 ; $i < count($playerIds); $i++){
            $crown = $this->dbConnecter->getCrowns($playerIds[$i]);
            array_push($crowns, $crown);
        }
        return $crowns;
    }

    function nextRound() {
        $this->dbConnecter->resetMove();
        $this->dbConnecter->increaseRound();
    }

    function checkWin($updatedCrown) {
        if($updatedCrown > 1){
            return TRUE;
        }
    }

    function playCard($playerId, $card) { // main function for the game flow
        if(!$this->isCardAvailable($playerId, $card)) {
            return;
        }
        $this->dbConnecter->setCard($playerId, $card);
        return $card;
    }

    function updateCards() {
        $cards = $this->getPlayedCards();
    }



    function checkGameState() {
        $gameState = $this->dbConnection->getGameState();
        // $this->response
    }

    function createPassword() {
        $pw = '';
        $characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
        for($i = 0; $i < 16; $i++) {
            $randomIndex = rand(0, strlen($characters));
            $pw .= $characters[$randomIndex];
        }
        // echo $pw;
        return $pw;
    }

    function checkId($playerId, $pw) {
        $storedPw = $this->dbConnecter->getPw($playerId);
        if(strcmp($pw, $storedPw)) {
            return TRUE;
        }
    }

    function addPlayer($nick) {
        $pw = $this->createPassword();
        $playerId = $this->dbConnecter->createPlayer($nick, $pw);
        $this->dbConnecter->increasePlayerCount();
        $this->dbConnecter->createMove($playerId);
        $playerInfo = array($playerId, $pw);
        return $playerInfo;
    }

    function isCardAvailable($playerId, $card) {
        $deck = $this->dbConnecter->getDeck($playerId);
        if($deck[$card] == '1') {
            return TRUE;
        }
    }


    function updateDecks($results) {
        $playerIds = $this->dbConnecter->getPlayerIds();
        $decks = array();
        for($i = 0; $i < count($playerIds); $i++) {
            $playerId = $playerIds[$i];
            $card = $this->dbConnecter->getCard($playerId);
            $result = $results[$i];
            $newDeck = $this->calcNewDeck($playerId, $card, $result);
            array_push($decks, $newDeck);
            $this->dbConnecter->updateDeck($playerId, $newDeck);
        }
        return $decks;
    }

    function updateCrowns($result) {
        $playerIds = $this->dbConnecter->getPlayerIds();
        for($i = 0; $i < count($result); $i++) {
            if($result[$i] == "win") {
                $playerId = $playerIds[$i];
                $newCrowns = $this->dbConnecter->addCrown($playerId);
                return $newCrowns;
            }
        }
    }

    function calcNewDeck($playerId, $card, $result) {
        $deck = $this->dbConnecter->getDeck($playerId);
        $stopIndex = $card;
        if($result == "win") {
            $stopIndex --;
        }
        for($i = 0; $i < $stopIndex; $i++) {
            $deck = $this->removeHighestCard($deck);
        }
        return $deck;
    }

    function removeHighestCard($deck) {
        for($i = 10; $i > 0; $i--) {
            if($deck[$i] == '1') {
                $deck[$i] = "0";
                return $deck;
            }
        }
        return $deck;
    }

    function getRoundResult() {
        $cards = $this->getPlayedCards();
        // $this->response->setPlayedCards($cards);
        $highest = $this->findHighestCard($cards);
        $occurrence = $this->getCardOccurrence($cards, $highest);
        $result = $this->calcRoundResult($cards, $highest, $occurrence);
        return $result;
    }

    function calcRoundResult($cards, $highest, $occurrence) {
        $result = array_fill(0, count($cards), "loss");
        if($occurrence == 1) {
            $index = array_search($highest, $cards);
            $result[$index] = "win";
        }
        else {
            for($i = 0; $i < count($cards); $i++) {
                if($cards[$i] == $highest) {
                    $result[$i] = "tie";
                }
            }
        }
        return $result;
    }

    function findHighestCard($cards) {
        return max($cards);
    }

    function getCardOccurrence($cards, $card) {
        $occurrence = 0;
        for( $i = 0; $i < count($cards); $i++) {
            if($cards[$i] == $card) {
                $occurrence ++;
            }
        }
        return $occurrence;
    }

    function allCardsPlaced() {
        $playerCount = $this->dbConnecter->getPlayerCount();
        $cards = $this->getPlayedCards();
        // print_r($cards);
        $placedCount = 0;
        for($i = 0; $i < count($cards); $i++) {
            $card = $cards[$i];
            if($card == '11') {
                continue;
            }
            $placedCount++;
        }
        // echo $playerCount;
        // echo "placed";
        // echo $placedCount;
        return $playerCount == $placedCount;
    }

    function checkMoveComplete(){
        $complete = $this->dbConnecter->checkMoveComplete();
        return $complete;
    }

    function getPlayedCards() {
        $playerIds = $this->dbConnecter->getPlayerIds();
        $cards = array();
        for($i = 0; $i < count($playerIds); $i++) {
            $newCard = $this->dbConnecter->getCard($playerIds[$i]);
            array_push($cards, $newCard);
        }
        return $cards;
    }
}

?>