<?php

class Player{
    public $name;
    public $game;
    public $cards;
    public $crowns;
    public $strategy;

    function __construct($name, $game, $strategy) {
        $this->name = $name;
        $this->game = $game;
        $this->cards = range(0, 10);
        $this->crowns = 0;
        $this->strategy = $strategy;
    }

    function playCard() {
        return call_user_func(array($this, $this->strategy));
    }

    function removeHighestCards($amount = 1) {
        for($i = 0; $i < $amount; $i++) {
            if (array_slice($this->cards, -1, 1, true) != 0) {
                array_pop($this->cards);
            }
        }
    }

    function removeCard($card) {
        $index = array_search($card, $this->cards);
        if ($index != 0) {
            array_splice($this->cards, $index);
        }
    }

    function addCrown() {
        $this->crowns += 1;
    }

    function changeName($newName) {
        $this->name = $newName;
    }

    function reset() {
        $this->cards = range(0, 10);
        $this->crowns = 0;
    }

    function randomBot() {
        $card = array_rand($this->cards);
        return $card;
    }

    function beaBot() {
        if($this->game->round == 0) {
            $card = 0;
        } elseif($this->game->round == 1) {
            $card = array_rand([0, 4]);
        } else {
            $card = max($this->cards);
        }
        return $card;
    }

    function niklasBot() {
        if($this->getRandomFloat() < 0.25) {
            if(in_array(1, $this->cards)) {
                $card = 1;
            } else {
                $card = 0;
            }
        } else{
            $card = 0;
        }
        return $card;
    }

    function henriekeBot() {
        if($this->game->round < 2) {
            $card = 0;
        } elseif($this->game->round == 2) {
            $card = 7;
        } else {
            $card = max($this->cards);
        }
        return $card;
    }

    function ausweglosBot() {
        if($this->game->round < 4) {
            $card = 0;
        } elseif($this->game->round == 4) {
            $card = 4;
        } else {
            $card = max($this->cards);
        }
        return $card;
    }

    function getRandomFloat() {
        return (float) mt_rand() / (float) mt_getrandmax();
    }
}
?>