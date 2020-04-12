<?php
$username = $_POST['username'];
$password = $_POST['password'];

#username = admin
#password = admin

if ($username == 'admin' && $password =='admin'){
    header("Location: admin/admin_index.html");
    exit;
}else{
    header("Location: admin_login.html");
    exit;
}

?>

