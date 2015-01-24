from ryu.base import app_manager 
# ofp_event 定义了事件，从而可以在函数中注册handler，监听事件，回应
from ryu.controller import ofp_event 
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls

class L2Switch(app_manager.RyuApp):
    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    # 修饰符用于说明修饰的函数应该被调用
    # parm1：事件发生时应该调用的函数，parm2：交换机握手后才可被调用
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    # 用于处理pack_in事件
    def packet_in_handler(self, ev):
        # 事件类ev中的msg用于携带触发事件的数据包
        msg = ev.msg

        # msg是packet_in报文, msg.datapath数据结构用于描述交换网桥(和控制器通信的实体单元)
        datapath = msg.datapath

        # datapath.ofproto对象是一个OpenFlow协议数据结构的对象，成员包含OpenFlow协议的数据结构，如动作类型OFPP_FLOOD
        ofp = datapath.ofproto

        # datapath.ofp_parser则是一个按照OpenFlow解析的数据结构
        ofp_parser = datapath.ofproto_parser

        # actions是一个列表，用于存放action list，可在其中添加动作。
        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        
        # 通过ofp_parser类，可以构造构造packet_out数据结构
        out = ofp_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=msg.in_port,
            actions=actions)
        
        # datapath.send_msg()函数用于发送数据到指定datapath
        datapath.send_msg(out)
