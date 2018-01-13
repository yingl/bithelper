<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);

include 'config.php';

$type = $wechat->getRev()->getRevType();
$openid = $wechat->getRevFrom();

switch($type) {
    case Wechat::MSGTYPE_TEXT: // Current use text to query coin info directly
        $code = $wechat->getRevContent();
        if (strcasecmp($code, 't5') == 0) {
            $data = $util->fetch_tops();
            $text = "当前最贵的5个币：\n" . $data['data'] . "\n";
            $text .= '更新时间' . $data['updated_at'];
            $wechat->text($text)->reply();
        }
        else if (strcasecmp($code, 'b5') == 0) {
            $data = $util->fetch_bottoms();
            $text = "当前最贵的5个币：\n" . $data['data'] . "\n";
            $text .= '更新时间' . $data['updated_at'];
            $wechat->text($text)->reply();
        }
        else if (in_array($code, $coins)) {
            $data = $util->fetch_code($code);
            $text = $code . ': ' . $data['price'] . "\n";
            $text .= '更新时间' . $data['updated_at'];
            $wechat->text($text)->reply();
        }
        else {
            $wechat->text('无法找到' . $code . '对应的币种')->reply();
        }
    case Wechat::MSGTYPE_EVENT:
        $event_array = $wechat->getRevEvent();
        $event_type = $event_array['event'];
        if ($event_type == 'subscribe') {
            $text = '欢迎访问比特小助手，数据来源OKEX，' . "\n";
            $text .= "数据刷新时间大约45~60秒。\n";
            $text .= "常用命令：\n";
            $text .= "- t5: 最贵的5个币（vs BTC）\n";
            $text .= "- b5: 最便宜的5个币（vs BTC）\n";
            $text .= '- ltc/xrp/...: 任意币的代码缩写，返回BTC报价。';
            $wechat->text($text)->reply();
        }
}

?>
