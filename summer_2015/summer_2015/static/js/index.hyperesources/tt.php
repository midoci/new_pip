<?php
/**
 * Created by PhpStorm.
 * User: alan
 * Date: 2014/12/24
 * Time: 10:38
 */
session_start();

if(!isset($_SESSION['location'])){
	$_SESSION['location']=0;
	$location = 0;
}

$location = $_SESSION['location'];

$arr=range(1,6);
shuffle($arr);
$location += $arr[0];

if($location > 108){
	$location -= 108;
}

$json['step'] = $arr[0];
$json['location'] = $location;

$_SESSION['location']=$location;

die(json_encode($json));

