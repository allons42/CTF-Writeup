<?php
// error_reporting(1);
function autoload($class) {
    @include_once(__DIR__.'/'.strtolower(str_replace('\\', '/', $class)).'.php');
}
spl_autoload_register('autoload');
session_start();

if (!isset($_GET['action']) || ($_GET['action'] == 'login' && (!isset($_POST['cb_user']) || !isset($_POST['cb_pass']))))
    die();

if ($_GET['action'] == 'login' && $_POST['cb_user'] == 'admin' && $_SERVER['REMOTE_ADDR'] != '127.0.0.1')
    die('access denied');

function require_admin() {
    if (!isset($_SESSION['admin']) || !$_SESSION['admin'])
        die('access denied');
}

switch ($_REQUEST['action']) {
    case 'login':
        if ($_POST['cb_user'] == 'admin' && !preg_match('/a/si', $_POST['cb_pass']) && md5($_POST['cb_pass']) == md5($_POST['cb_salt'].'a')) {
            $_SESSION['admin'] = true;
            die(lib\Flag::FLAG1);
        } else
            die('try harder');
        break;
    case 'save_item':
        require_admin();

        $item_name = $_POST['item']['name'];
        $item_uuid = $_POST['item']['uuid'];
        $item_content = $_POST['item']['content'];
        $item_filename = 'up/'.substr(md5($item_name),0,4).'.php';

        if (!preg_match('/^[a-zA-Z0-9]*$/', $item_name) || !preg_match('/^\S{8}-\S{27}$/', $item_uuid))
            die('blanket and special characters is not allowed in item name or uuid is invalid');

        $db = new lib\DB();
        if ($db->query("INSERT INTO items (`name`, `uuid`, `filename`) VALUES ('$item_name', '$item_uuid', '$item_filename')")) {
            @file_put_contents($item_filename, $item_content);
            die('success');
        }
        else
            die('internal server error');
    case 'list_item':
        require_admin();
        
        $db = new lib\DB();
        $res = $db->query("SELECT * FROM items");
        if (!$res)
            die('error');

        while ($row = mysqli_fetch_assoc($res)) {
            echo '--- start '.$row['name'].' '.$row['uuid'].' ---<br/>';
            echo 'Content: '.file_get_contents($row['filename']).'<br/>';
            echo '---  end  '.$row['name'].' '.$row['uuid'].' ---<br/><br/>';
        }
        break;
    default:
        die('unsupported action');
}
?>