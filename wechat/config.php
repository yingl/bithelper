<?php

include 'lib/dao.class.php';
include 'lib/wechat.class.php';
include 'lib/util.class.php';

define('HOME_FOLDER', 'bithelper');

$coins = array('ltc',
               'eth',
               'etc',
               'bch',
               'xrp',
               'xem',
               'xlm',
               'iota',
               '1st',
               'aac',
               'ace',
               'act',
               'amm',
               'ark',
               'ast',
               'avt',
               'bcd',
               'bcx',
               'bnt',
               'btm',
               'cag',
               'cmt',
               'ctr',
               'cvc',
               'dash',
               'dat',
               'dgb',
               'dgd',
               'dna',
               'dnt',
               'dpy',
               'edo',
               'elf',
               'eng',
               'eos',
               'evx',
               'fair',
               'fun',
               'gas',
               'gnt',
               'gnx',
               'hsr',
               'icn',
               'icx',
               'itc',
               'kcash',
               'knc',
               'lend',
               'link',
               'lrc',
               'mag',
               'mana',
               'mco',
               'mda',
               'mdt',
               'mot',
               'mth',
               'mtl',
               'nas',
               'neo',
               'nuls',
               'oax',
               'omg',
               'pay',
               'ppt',
               'pro',
               'qtum',
               'qvt',
               'rcn',
               'rct',
               'rdn',
               'read',
               'req',
               'rnt',
               'salt',
               'san',
               'sbtc',
               'show',
               'smt',
               'sngls',
               'snm',
               'snt',
               'ssc',
               'storj',
               'sub',
               'swftc',
               'tnb',
               'trx',
               'ubtc',
               'ugc',
               'ukg',
               'utk',
               'vee',
               'vib',
               'wrc',
               'wtc',
               'xmr',
               'xuc',
               'yoyo',
               'zec',
               'zrx');

$dao_options = array('dsn' => 'mysql:host=localhost;dbname=bithelper;',
                     'username' => 'root',
                     'password' => '',
                     'options' => array(PDO::MYSQL_ATTR_INIT_COMMAND => 'set names utf8'));
$dao = new DAO($dao_options);

function logdebug($text) {
    file_put_contents($_SERVER['DOCUMENT_ROOT'] . '/' . HOME_FOLDER . '/log.txt',
                      $text. "\n",
                      FILE_APPEND);
}

$wechat_options = array('appid' => 'wxf3051f460146fdd3',
                        'appsecret' => '50a415f994a828629104db9e71fe5323',
                        'token' => 'bithelper',
                        'debug' => true,
                        'logcallback' => 'logdebug');
$wechat = new Wechat($wechat_options);

$util = new Util($dao);

?>
