<?php
require __DIR__ . '/vendor/autoload.php';

$app = AppFactory::create();


$app->get('/fruits',function($request,$response){
    $fruits = ['apple','banana','mango'];
    $response->getBody()->write(json_encode($fruits));
    return $response->withHeader('Content-Type','application/json');
});

$app->post('/fruits',function($request,$response){
    $data = $request->getParsedBody();
    $fruits = $data['fruit'] ?? null;

    if($fruits){
        $response->getBody()->write(json_encode(['status'=>'success','fruit'=>$fruits]));
    }else{
        $response->getBody()->write(json_encode(['status'=>'error','message'=>'No fruit provided']));
    }
    return $response->withHeader('Content-Type','application/json');
});

$app->run();