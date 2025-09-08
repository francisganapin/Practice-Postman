<?php

header('Content-type:application/json');

$data=[
    'status' => 'success',
    'message' =>'Welcome to my PHP api',
    'time' => date('Y-m-d h:i:s')
];

echo json_encode($data);