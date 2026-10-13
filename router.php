<?php
$uri = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH) ?: '/');
$root = __DIR__;
$requested = realpath($root . $uri);

if ($uri !== '/' && $requested && str_starts_with($requested, $root) && is_file($requested)) {
    if (strtolower(pathinfo($requested, PATHINFO_EXTENSION)) === 'html') {
        header('Content-Type: text/html; charset=UTF-8');
        header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
        header('Pragma: no-cache');
        readfile($requested);
        return true;
    }
    return false;
}

if ($uri === '/' || $uri === '/index.html') {
    header('Content-Type: text/html; charset=UTF-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Pragma: no-cache');
    readfile($root . '/index.html');
    return true;
}

$routes = [
    '/catalogo' => 'catalogo.html',
    '/catalogo/diagnostica' => 'categoria.html',
    '/categoria' => 'categoria.html',
    '/catalogo/prodotti/gima-49876' => 'prodotto.html',
    '/prodotto' => 'prodotto.html',
    '/soluzioni-per-ente' => 'soluzioni.html',
    '/soluzioni-per-organizzazioni' => 'soluzioni.html',
    '/soluzioni' => 'soluzioni.html',
    '/mepa' => 'mepa.html',
    '/acquista-su-mepa' => 'mepa.html',
    '/come-acquistare' => 'come-acquistare.html',
    '/chi-siamo' => 'chi-siamo.html',
    '/referenze' => 'referenze.html',
    '/contatti' => 'contatti.html',
    '/faq' => 'faq.html',
    '/domande-frequenti' => 'faq.html',
    '/lista-quotazione' => 'lista-quotazione.html',
];

$normalized = rtrim($uri, '/') ?: '/';
if (isset($routes[$normalized]) && is_file($root . '/' . $routes[$normalized])) {
    header('Content-Type: text/html; charset=UTF-8');
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Pragma: no-cache');
    readfile($root . '/' . $routes[$normalized]);
    return true;
}

http_response_code(404);
header('Content-Type: text/html; charset=UTF-8');
echo '<!doctype html><html lang="it"><meta charset="utf-8"><title>Pagina non trovata | MedicalMade</title><body><h1>Pagina non trovata</h1><p><a href="/">Torna alla home</a></p></body></html>';
return true;
