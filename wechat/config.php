<?php

include 'lib/dao.class.php';
include 'lib/wechat.class.php';
include 'lib/util.class.php';

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

$dao_options = ['dsn' => 'mysql:host=localhost;dbname=bithelper;',
                'username' => 'root',
                'password' => '',
                'options' => [PDO::MYSQL_ATTR_INIT_COMMAND => 'set names utf8']];
$dao = new DAO($dao_options);

function logdebug($text) {
    file_put_contents($_SERVER['DOCUMENT_ROOT'] . '/log.txt',
                      $text. "\n",
                      FILE_APPEND);
}

$wechat_options = ['appid' => 'wxf3051f460146fdd3',
                   'appsecret' => 'TODO',
                   'token' => 'bithelper',
                   'debug' => true,
                   'logcallback' => 'logdebug'];
$wechat = new Wechat($wechat_options);

$util = new Util($dao);

?>
