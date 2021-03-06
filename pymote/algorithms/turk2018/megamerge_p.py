# -*- coding: utf-8 -*-
#12:45
from pymote.algorithm import NodeAlgorithm
from pymote.message import Message
from pymote import Node
from random import random
import collections
from sys import maxint
from pymote.algorithms.turk2018.test_helper import prepare_absorption, prepare_friendly_merger

class MegaMerger(NodeAlgorithm):
    required_params = ()
    default_params = {'neighborsKey': 'Neighbors', 'treeKey': 'TreeNeighbors', 'parentKey' : 'Parent', 'weightKey': 'Weight',
    'levelKey': 'Level', 'nameKey': 'Name', 'debugKey': 'DEBUG' , 'linkStatusKey':'LinkStatus', 'nodeEdgeKey': 'MinimumEdgeNode',
    'reportCounterKey': 'ReportCounter', 'numberOfInternalNodesKey': 'NumberOfInternalNodes', 'Let_us_merge_FriendlyMergerKey': 'Let_us_merge',
    'friendlyMergerMessagekey': 'FriendlyMergerMessage', 'let_us_merge_queue_key': 'Let_us_merge_queue', 'lateKey': 'late', 'blockedKey': 'Blocked'}

    def initializer(self):
        ini_nodes = []
        max_node = Node()
        for node in self.network.nodes():
            node.memory[self.neighborsKey] = node.compositeSensor.read()['Neighbors']
           #node.memory[self.treeKey] = list(node.memory[self.neighborsKey])
            self.initialize(node)
            node.status = 'AVAILABLE'
            '''if random()<0.3:                #random initializers
                node.status = 'AVAILABLE'
                ini_nodes.append(node)'''

        # just for testing purposes
        #prepare_absorption(self)
        #prepare_friendly_merger(self)



        # starting node has lover lvl for absorpton to work
        
        ini_nodes.append(self.network.nodes()[7])
        ini_nodes.append(self.network.nodes()[0])
        ini_nodes.append(self.network.nodes()[1])
        ini_nodes.append(self.network.nodes()[4])
        ini_nodes.append(self.network.nodes()[2])
        ini_nodes.append(self.network.nodes()[6])
        ini_nodes.append(self.network.nodes()[5])
        ini_nodes.append(self.network.nodes()[3])



        
        for ini_node in ini_nodes:
            self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI,destination=ini_node))  # to je spontani impuls
        
        
        # ne znam kako radi ovaj ini_nodes YOLO
        #ini_node = self.network.nodes()[1]                                                         ### 0. ili 1. imalvl 1? odluci se
        #self.network.outbox.insert(0, Message(header=NodeAlgorithm.INI,destination=ini_node))

    def available(self, node, message):

        #inicijatori
        if message.header == NodeAlgorithm.INI: #Spontaneously
            # koristimo za test absorptiona
            #prepared_data = self.prepare_message_data_concatenate(node)
            #for testing send Let us merge to the first neighbor.
            #node.send(Message(header='Let Us Merge', data=0, destination=node.memory[self.neighborsKey][0]))
            #node.send(Message(header='Let Us Merge', data=0, destination=node.memory[self.neighborsKey][1])) 
            ## Iskljucivo inicijatori, bilo jedan ili svi poslat ce svom prvom i drugm susjedu Let Us Merge
            self.send_Outside(node)

        if message.header=='Outside?':
            self.check_Outside_header(node, message)
            self.send_Outside(node, message)

        # ja ne kuzim kako rade ovi statusi stvarno
        if message.header=="Let Us Merge":
            #self.process_message_check_levels(node,message)
            #self.resolve(node, message)
            pass


        node.status = 'PROCESSING'

        '''node.send(Message(header='Activate', data='Activate'))
        if len(node.memory[self.neighborsKey])==1 : #ako je čvor list
            node.memory[self.parentKey] = list(node.memory[self.neighborsKey])[0]
            updated_data=self.prepare_message(node)
            node.send(Message(header='M', data = updated_data, destination = node.memory[self.parentKey]))
            node.status = 'PROCESSING'
        else:
            node.status = 'ACTIVE' #izvrši se

    if message.header == 'Activate':
        destination_nodes = list(node.memory[self.treeKey])

        destination_nodes.remove(message.source)
        node.send(Message(header='Activate', data='Activate', destination=destination_nodes))
        if len(node.memory[self.treeKey])==1 :
            node.memory[self.parentKey] = list(node.memory[self.treeKey])[0]
            updated_data=self.prepare_message(node)
            node.send(Message(header='M', data=updated_data, destination=node.memory[self.parentKey]))
            node.status = 'PROCESSING'
        else:
            node.status='ACTIVE' #izvrši se'''

    def active(self, node, message):
        '''if message.header=='M':
            self.process_message(node,message)
            node.memory[self.treeKey].remove(message.source)
            if len(node.memory[self.treeKey])==1 :
                node.memory[self.parentKey] = list(node.memory[self.treeKey])[1]
                updated_data=self.prepare_message(node)
                node.send(Message(header='M', data=updated_data, destination=node.memory[self.parentKey]))
                node.status = 'PROCESSING' '''
        pass

    def processing(self, node, message):
        # valjda ovo rjesava donji TODO
        if message.header=='Outside?':
            node.memory['mozdavise'] = 'usao sam'
            self.check_Outside_header(node, message)
            self.send_Outside(node, message)

        #TODO add Outside? for other nodes, not just INI_NODES
        if message.header=="Let_us_merge":
            #           ako je poruka iz istog grada salji dalje, ako nije onda je to mergeEdge
            if node.memory[self.linkStatusKey][message.source] == 'INTERNAL':
                node.memory[self.debugKey] = 'YOLO'
#               we can't use destination_node in previous if because inital values of nodeEdgeKeys are the nodes themselves.
                destination_node = node.memory[self.nodeEdgeKey].keys()[0]
#               special case yeaaah. this sucks :( . Because node a will compute friendly merger, when b recieves Let_us_merge he we will 
#               use a's data, a a je vec povecao lvl. Ili promijeniti svugdje nacin slanja ili samo za ovaj specificni slucaj. Potrebno je 
#               imati i handler za ovaj slucaj.
                prepared_data = self.check_and_prepare_data(node)
                node.send(Message(header='Let_us_merge', data=prepared_data, destination=destination_node))
            else:
                self.check_unblock(node, message.source)
                self.process_message_check_levels(node,message)

#           hardcoding :( . if we get let_us_merge and we are merging egde, we will remember it 
#           because we may need it for friendly merger. We need to set this somewhere.
#           TODO make this readable at least
#           because friendly merger resets Let_us_merge... we are going to check for default value first.
            if node.memory[self.Let_us_merge_FriendlyMergerKey] == False:
                if node.memory[self.nodeEdgeKey].keys()[0] in node.memory[self.linkStatusKey]:
                    if node.memory[self.linkStatusKey][message.source] == 'INTERNAL':
                        if node.memory[self.linkStatusKey][node.memory[self.nodeEdgeKey].keys()[0]] == 'EXTERNAL':
                            self.change_let_us_merge_FriendlyMergerKey(node, True)

            else:
#               if node is the root we would double the level check
                if node.memory[self.linkStatusKey][message.source] == 'INTERNAL' and node.memory[self.parentKey] != None:
                    node.memory[self.debugKey] = 'pogodak'
                    self.process_message_check_levels(node, node.memory[self.friendlyMergerMessagekey])


        if message.header=="absorption+orientation_of_roads" or message.header=="absorption":
            self.check_unblock(node)
            self.change_name_level(node, message)
            self.absorption(node, message)
            if message.header=="absorption+orientation_of_roads":
                #REDOSLJED FUNKCIJA MORA BITI OVAKAV. Prvo posaljemo parentu poruku, onda maknemo parenta.
                self.absorption(node, message, False, True)
                node.memory[self.parentKey] = message.source
#           TEST - start next cycle
            self.send_Outside(node)

        if message.header=="friendly_merger+orientation_of_roads" or message.header=="friendly_merger":
            self.check_unblock(node)
            self.change_name_level(node, message)
            self.friendly_merger(node, message)
            if message.header=="friendly_merger+orientation_of_roads":
                self.friendly_merger(node, message, False, True)
                node.memory[self.parentKey] = message.source
            self.send_Outside(node)


        #TODO or internal external suspension
        if message.header=="Internal":
            self.change_link_status_key_internal(node, message.source)
        elif message.header=="External":
            self.change_link_status_key_external(node, message.source)
            if node.memory[self.parentKey]!=None:
#               iako je provjera za parenta isto u metodi ispod, potrebna nam je iznad
                #if self.check_if_city_has_one_node(node):
                self.check_report(node)
                #node.send(Message(header='Report', data=0, destination=node.memory[self.parentKey]))
            else:
#               TODO when merging egde is also downtown - WRONG, he should be sending let us merge. this is a quick fix for merge node being root.
                self.change_let_us_merge_FriendlyMergerKey(node, True)
                node.send(Message(header="Let_us_merge" ,data=0, destination=message.source))
                node.memory['DEBUG2'] = 'external root'

        if message.header=="Report":
            node.memory[self.reportCounterKey] += 1
            #node.memory[self.nodeEdgeKey] = self.min_weight_two_nods(node.memory[self.nodeEdgeKey], message.source, node)
            self.min_weight_two_nods(node.memory[self.nodeEdgeKey], message.source, node)
            self.check_report(node)

    def saturated(self, node):
        pass

    def prepare_message(self,node):
        pass

    '''def prepare_message_data_concatenate(self, node):
      
        args = {self.nameKey: node.memory[self.nameKey], self.levelKey: node.memory[self.levelKey]}
        #data = ",".join(args)
        return args'''

    def process_message(self, node, message):
        pass

    def send_Outside(self, node, message = None):
        #TODO everytime node receive Internal, send message again somehow TEST
        #if multiple same edge has been choosen and already Outside message exists, then we dont have to do anything
        test = self.min_weight(node, message)
        if test == None:
            return
        else:
            node.memory[self.nodeEdgeKey] = test
#       if the choosen merge dge is the first one in queue pop it
        if len(node.memory[self.let_us_merge_queue_key]) > 0:
            if node.memory[self.nodeEdgeKey] == node.memory[self.let_us_merge_queue_key][0].source:
                node.memory[self.let_us_merge_queue_key].popleft()
        #node.memory[self.debugKey] = node.memory[self.nodeEdgeKey]
        #node.memory[self.debugKey] = 'zakaj sam ja tu usao?'
        # solution for infinitive is {self node: [maxint, maxint]}. we don't want node to send message to itself, we want to report it
#       to parent as infinitive. Of course if no parent present otherwise it just sends to everyone
#       if outside is the same edge as the one we just sent External to then we can skip this adn send Let_us_merge
#       TODO we will not use this behaviour for now. It creates a lot of problems. Return stays otherwise node sends Outisde? with no reason.
        if message != None:
            if node.memory[self.nodeEdgeKey].keys()[0] == message.source:
#               currently buggy
                #node.send(Message(header="Let_us_merge" ,data=0, destination=message.source))
                #self.change_let_us_merge_FriendlyMergerKey(node, True)
                #return
                pass
        if node.id != node.memory[self.nodeEdgeKey].keys()[0].id and not self.check_outbox_External_exists(node):
            node.send(Message(header='Outside?', data=0, destination=node.memory[self.nodeEdgeKey]))
#           mislim da je kasno samo u slucaju  reportanja.
            #node.memory[self.lateKey] = True
            node.memory['ooutside'] = node.memory[self.lateKey]
            node.memory[self.blockedKey] = True
#       if node is the only member of the city we dont need reports.
        #elif self.check_if_city_has_one_node(node):
            #self.check_report(node)
            #node.send(Message(header='Report', data=0, destination=node.memory[self.parentKey]))

        #node.memory[self.nodeEdgeKey] = {node.memory[self.weightKey].keys()[0]: node.memory[self.weightKey].values()[0]}
        #node.send(Message(header='Outside?', data=0, destination=node.memory[self.nodeEdgeKey]))

#   it's a duplicate in 2 states, available and processing
    def check_Outside_header(self, node, message):
        if message.source.memory[self.nameKey]==node.memory[self.nameKey]:
                node.send(Message(header='Internal', data=0, destination=message.source))
                self.change_link_status_key_internal(node, message.source)
        elif node.memory[self.levelKey] >= message.source.memory[self.levelKey]:
            node.send(Message(header='External', data=0, destination=message.source))
            self.change_link_status_key_external(node, message.source)
            #self.check_outbox_Outside_remove_redundant(node, temp_message)
        else:
#           if the merge egde is the one being suspended, node would always pick that edge for merge.
            #self.change_link_status_key_external(node, message.source)
            node.memory[self.let_us_merge_queue_key].append(message)

#   duplicate in send_Outside and Report case in Processing. If it's the leaf node then check if we can start sending reports back.
#   if we send report back or we receive all reports then it' to late to start new bestMergeEgdeFinding in case of an absorption
#   TODO check if 2 ifs below are not redundant
    def check_report(self, node):
        node.memory['check_report'] = node.memory[self.lateKey]
        if (node.memory[self.reportCounterKey]>=node.memory[self.numberOfInternalNodesKey]-1 and node.memory[self.parentKey] != None and 
        node.memory[self.numberOfInternalNodesKey] >= len(node.memory[self.neighborsKey])):
            node.send(Message(header='Report', data=0, destination=node.memory[self.parentKey]))
            node.memory[self.reportCounterKey] = 0
            node.memory[self.lateKey] = True
        if (node.memory[self.reportCounterKey]>=node.memory[self.numberOfInternalNodesKey] and node.memory[self.parentKey] == None and
        node.memory[self.numberOfInternalNodesKey] >= len(node.memory[self.neighborsKey])):
            #TODO END if given weights are both maxint for root
            if (node.memory[self.nodeEdgeKey].values()[0][0] == maxint and 
                node.memory[self.nodeEdgeKey.values()[0][1]] == maxint):
                    pass
            node.send(Message(header='Let_us_merge', data=0, destination=node.memory[self.nodeEdgeKey].keys()[0]))
            node.memory[self.reportCounterKey] = 0
            node.memory[self.lateKey] = True

    def check_if_city_has_one_node(self, node):
        counter = 0
        counter = sum(value == 'INTERNAL' for value in node.memory[self.linkStatusKey])
        if counter > 0:
            return True
        else:
            if node.memory[self.parentKey] != None:
                return True
            else:
                return False

    def check_and_prepare_data(self, node):
        if (node.memory[self.Let_us_merge_FriendlyMergerKey] == False):
            prepared_data = 0
        else:
            prepared_data = {'Level': node.memory[self.levelKey]}

#   mutiple Outside message can be possible because of multiple send_Outisde calls.
    def check_outbox_Outside_exists(self, node):
        if len(node.outbox) > 0:
            node.memory['DEBUG3'] = node.outbox[0].header
        else:
            return False
        #return any(message.header=="Outside?" for message in node.outbox)
        #return (True if message.header=="Outside?" else False for message in node.outbox)
        for message in node.outbox:
            #node.memory['listDebug'].append(message.header)
            if message.header=='Outside?':
                return True
        return False
#   explanation in check_Outside_header
    def check_outbox_Outside_remove_redundant(self, node, external_message):
        if len(node.outbox) <= 1:
            return
        for message in node.outbox:
            if external_message.destination == message.destination and message.header == "Outside?":
                node.outbox.remove(message)

#   if outside message is being sent on the same edge is reduntant and creates problems
#   it happens when node answers external and the same edge is chosen as merge edge
    def check_outbox_External_exists(self, node):
        if len(node.outbox) <= 0:
            return False
        node.memory['debug222'] = node.outbox
        for message in node.outbox:
            if message.destination.id == node.memory[self.nodeEdgeKey].keys()[0].id and message.header=="External":
                return True
                node.memory['debug222'] = 'da'
        return False

    def check_unblock(self, node, mergeNode=None):
        if node.memory[self.blockedKey] == False:
            return
        if not mergeNode:
            node.memory[self.blockedKey] = False
        else:
            if node.memory[self.nodeEdgeKey].keys()[0].id == mergeNode.id:
                node.memory[self.blockedKey] = False

#   name and level changes are in a function because they will be reused and we need to 
#   check queue whenever level changes
#   reset comes first beacuse of check_queue method which gets wrong memory info regarding lateKey
#   what_is_it: is it absorption or friendly merger?
    def change_name_level(self, node, message=None, city_name = None, what_is_it='absorption'):
        self.reset(node)
        if what_is_it == 'absorption':
            node.memory[self.nameKey] = message.source.memory[self.nameKey]
            node.memory[self.levelKey] = message.source.memory[self.levelKey]
        elif what_is_it == 'friendly_merger':
            node.memory[self.nameKey] = city_name
            node.memory[self.levelKey] += 1
            if len(node.memory[self.let_us_merge_queue_key]) > 0 :
                self.check_queue(node)

#   put here everything that needs to be reset after absorption or friendly merger happens
#   TODO fidn out what else needs to be reset
    def reset(self, node):
        self.change_let_us_merge_FriendlyMergerKey(node, False)
        node.memory[self.lateKey] = False

#   TODO if lvl is greater then absorb th other city. Absorption calls send_Outside which calls min_weight which calls check_queue again
#   so it will repeat itself. Also in min_weight there is a check for the same level.
#   if header is Outside? than we just need to reply.
    def check_queue(self, node):
#       it worked without this somehow, now it doesn't
        if len(node.memory[self.let_us_merge_queue_key]) < 1:
            return
        node.memory['prvo'] = 'prvo'
        if node.memory[self.let_us_merge_queue_key][0].header=="Outside?":
            node.memory['dugo'] = 'drugo'
            if node.memory[self.levelKey] >= node.memory[self.let_us_merge_queue_key][0].source.memory[self.levelKey]:
                #self.check_Outside_header(node, node.memory[self.let_us_merge_queue_key].popleft())
#               function check_Outside_header does some more things so i dont want t want to risk it
                #self.change_link_status_key_external(node, node.memory[self.let_us_merge_queue_key][0].source)
                #node.send(Message(header='External', data=0, destination=node.memory[self.let_us_merge_queue_key].popleft().source))
                self.check_Outside_header(node, node.memory[self.let_us_merge_queue_key].popleft())
        elif node.memory[self.levelKey] > node.memory[self.let_us_merge_queue_key][0].source.memory[self.levelKey]:
            self.absorption(node, node.memory[self.let_us_merge_queue_key].popleft(), True)

#   late flag will be raised whenever report is being sent to parent or node sends Outside message or better whenever it has
#   finished computating mergeEdge.
#   One special case is when absorption is beign made on the chosen merge edge for the node. Thenically, then
#   it was not in a queue and it solved suspension for that edge so we continue with computing new merge edge(
#   late flag is down now)
    def check_and_send_late_absorption(self, node, header, destination):
        node.memory['debug2323'] = node.memory[self.lateKey
        ]
        if node.memory[self.lateKey] == True and node.memory[self.nodeEdgeKey].keys()[0].id != destination.id:
                node.send(Message(header=header+"+late", data=0, destination=destination))
        else:
            node.send(Message(header=header, data=0, destination=destination))
        if node.memory[self.nodeEdgeKey].keys()[0].id == destination:
            node.memory[self.lateKey] = False
            if self.check_if_city_has_one_node(node):
                self.check_report(node)

#   equal = frendly merger or suspenson, smaller = absorption, bigger = never happens
#   special_case handler is here. 
    def process_message_check_levels(self, node, message):
        special_case_boolean = False
        if message.data != 0:
            if message.data['Level'] == node.memory[self.levelKey]:
                special_case_boolean = True
        if message.source.memory[self.levelKey] < node.memory[self.levelKey]:
            self.absorption(node, message, True)
        elif message.source.memory[self.levelKey] == node.memory[self.levelKey] or special_case_boolean == True:
            if node.memory[self.nodeEdgeKey].keys()[0].id == message.source.id or node.memory[self.nodeEdgeKey].keys()[0].id == node.id:
                node.memory[self.debugKey] = "ovdje?"
    #           if friendly merger and the node is the root we need to procesde with friendly merger.
                if node.memory[self.Let_us_merge_FriendlyMergerKey] == True or node.memory[self.parentKey] == None:
                    self.friendly_merger(node, message, True)
                else:
                    self.change_let_us_merge_FriendlyMergerKey(node, True)
                    node.memory[self.friendlyMergerMessagekey] = message
#           suspension and put in queue
            else:
                node.memory['DEBUG2'] = 'suspension'
                node.memory[self.let_us_merge_queue_key].append(message)
        else:
            node.memory['DEBUG2'] = 'other susension'
#           ovaj se nikad ne bi trebao dogoditi
            pass

    def change_link_status_key_internal(self, node, message_source):
        node.memory[self.linkStatusKey][message_source] = "INTERNAL"
        node.memory[self.numberOfInternalNodesKey] += 1
    def change_link_status_key_external(self, node, message_source):
        node.memory[self.linkStatusKey][message_source] = "EXTERNAL"

    def change_let_us_merge_FriendlyMergerKey(self, node, TRUE=False):
        if TRUE == True:
            node.memory[self.Let_us_merge_FriendlyMergerKey] = True
        else:
            node.memory[self.Let_us_merge_FriendlyMergerKey] = False

#   param begining - pocetnio slanje
#   orientation_of_rodas - Ako saljemo parentu, trebamo promijeniti orientaciju do roota. drugi cvorovi koji nisu na putu
#       zbog uvjeta slanja poruka nece slati poruke parentima, osim ako vujet niej True.
    def absorption(self, node, message, param_begining=False, orientation_of_roads=False):
        if node.memory[self.linkStatusKey][message.source]=='EXTERNAL':
            self.change_link_status_key_internal(node, message.source)
            if param_begining==True:
                node.memory['i am alte'] = node.memory[self.lateKey]
                self.check_and_send_late_absorption(node, "absorption+orientation_of_roads", message.source)
                #node.send(Message(header="absorption+orientation_of_roads", data=0, destination=message.source))
                self.send_Outside(node)
        else:
            if orientation_of_roads==True:
                if node.memory[self.parentKey]!=None:
                    #node.send(Message(header="absorption+orientation_of_roads", data=0, destination=node.memory[self.parentKey]))
                    self.check_and_send_late_absorption(node, "absorption+orientation_of_roads", node.memory[self.parentKey])
                else:
                    # DEBUG
                    node.memory[self.debugKey] = "Nemam parenta"
            else:
                destination_nodes = list(filter(lambda neighbor:  neighbor != node.memory[self.parentKey] and neighbor != message.source
                    and node.memory[self.linkStatusKey][neighbor] == 'INTERNAL', node.memory[self.neighborsKey])) 
                #node.send(Message(header="absorption", data=0, destination=destination_nodes))
                self.check_and_send_late_absorption(node, "absorption", destination_nodes)

#   compute new downtown (smaller ID) from two nodes independently one form antoher. add new name and increase lvl by one.
#   we need to change the orientation of roads depending on which node is the new downtown, also change internal nodes
    def friendly_merger(self, node, message, param_begining=False, orientation_of_roads=False):
        if param_begining == True:
#            Only when node is the root
            if node.memory[self.Let_us_merge_FriendlyMergerKey] == False:
                node.send(Message(header='Let_us_merge', data={'Level': node.memory[self.levelKey]}, destination=message.source))
            b = message.source
            new_downtown = self.min_id_two_nodes(node, b)
            self.change_name_level(node, None, new_downtown.id, 'friendly_merger')
            self.change_link_status_key_internal(node, b)
#           without parent, message is being sent to everyone!!
            if node.memory[self.parentKey] != None:
                node.send(Message(header="friendly_merger+orientation_of_roads", data=0, destination=node.memory[self.parentKey]))
#           because we change parent, we need to send the message first.
            if new_downtown.id != node.id:
                node.memory[self.parentKey] = b
            else:
                node.memory[self.parentKey] = None
            node.memory['I am late'] = node.memory[self.lateKey]
            self.send_Outside(node)
        else:
            if orientation_of_roads == True: 
                if node.memory[self.parentKey] != None:
                    node.send(Message(header="friendly_merger+orientation_of_roads", data=0, destination=node.memory[self.parentKey]))
                else:
                    pass
            else:
                destination_nodes = list(filter(lambda neighbor:  neighbor != node.memory[self.parentKey] and neighbor != message.source
                    and node.memory[self.linkStatusKey][neighbor] == 'INTERNAL', node.memory[self.neighborsKey])) 
                node.send(Message(header="friendly_merger", data=0, destination=destination_nodes))


    def initialize(self, node):
        node.memory[self.weightKey] = {}
        node.memory[self.linkStatusKey] = {}
        node.memory[self.levelKey] = 0
        node.memory[self.nameKey] = node.id
        node.memory[self.parentKey] = None
        node.memory[self.reportCounterKey] = 0
        node.memory[self.numberOfInternalNodesKey] = 0
        node.memory[self.Let_us_merge_FriendlyMergerKey] = False
        node.memory[self.friendlyMergerMessagekey] = False
        # sam sebe dodamo kao defaultni minimumEdgeNode sa max weightom.
        node.memory[self.nodeEdgeKey] = {node: [maxint, maxint]}
        node.memory[self.let_us_merge_queue_key] = collections.deque([])
        node.memory[self.lateKey] = False
        node.memory[self.blockedKey] = False
        for neighbor in node.memory[self.neighborsKey]:
            node.memory[self.weightKey][neighbor] = [min(node.id, neighbor.id),
            max(node.id, neighbor.id)]

        for neighbor in node.memory[self.neighborsKey]:
            node.memory[self.weightKey][neighbor] = [min(node.id, neighbor.id),max(node.id, neighbor.id)]
            node.memory[self.linkStatusKey][neighbor] = "UNUSED"


    def min_weight(self,node, message):
#       check queue
        if len(node.memory[self.let_us_merge_queue_key]) > 0 :
            node.memory['min_weight_2'] = node.memory[self.nodeEdgeKey]
            self.check_queue(node)

#       check if Outside? message already exists in inbox
        if self.check_outbox_Outside_exists(node):
            node.memory['DEBUG5'] = 'wtf'
            return None

        node.memory[self.debugKey] = node.memory[self.nodeEdgeKey]
        #TODO if no unused edge found, return infinitive weight TEST
        #we are considering only unused edges.
        temp_unused_external_edges = dict()
        temp_node = None

#       trick to add just changed extrnal edge to what it should be while in this method, an unused edge. if just added external edge is suspensed
#       then dont include it.
        '''if len(node.memory[self.let_us_merge_queue_key]) > 0:
            if message != None and message.source.id != node.memory[self.let_us_merge_queue_key][0].source.id:
                node.memory[self.linkStatusKey][message.source] = 'UNUSED'
        else:
            if message != None:
                node.memory[self.linkStatusKey][message.source] = 'UNUSED' '''

        #if self.check_outbox_External_exists(node):
            #node.memory[self.linkStatusKey][node.memory[self.nodeEdgeKey].keys()[0]] = 'UNUSED'
        if node.memory[self.blockedKey] == True:
            return None
#       if same levels in queue then include it for me
        if len(node.memory[self.let_us_merge_queue_key]) > 1:
            if node.memory[self.levelKey] == node.memory[self.let_us_merge_queue_key][0].source.memory[self.levelKey]:
                temp_node = node.memory[self.let_us_merge_queue_key][0].source
        #temp_unused_edges = [(k, v) if v2='UNUSED' for (k,v), (k, v2) in zip(node.memory[self.weightKey].items(), node.memory[self.linkStatusKey].items())]
        for k,v in node.memory[self.weightKey].iteritems():
            if node.memory[self.linkStatusKey][k] == 'UNUSED' or node.memory[self.linkStatusKey][k] == temp_node:
                temp_unused_external_edges[k] = v
        #if message != None:
            #node.memory[self.linkStatusKey][message.source] = 'EXTERNAL'
        '''if len(node.memory[self.let_us_merge_queue_key]) > 0:
            if message != None and message.source.id != node.memory[self.let_us_merge_queue_key][0].source.id:
                node.memory[self.linkStatusKey][message.source] = 'EXTERNAL'
            else:
                if message != None:
                    node.memory[self.linkStatusKey][message.source] = 'EXTERNAL' '''
        #if self.check_outbox_External_exists(node):
            #node.memory[self.linkStatusKey][node.memory[self.nodeEdgeKey].keys()[0]] = 'EXTERNAL'
#       TEST - solution for TODO 
        if not temp_unused_external_edges:
            infinitiveEdge = {node: [maxint,maxint]}
            return infinitiveEdge
        orderedDict = collections.OrderedDict(sorted(temp_unused_external_edges.iteritems(), key=lambda (k,v):v[0]))            
        min_1= orderedDict.values()[0][0]
        print(min_1)        
        uzi_izbor={}

#        print("sortirano 1 ")               
        for o in orderedDict:
            #print orderedDict[o]
            if orderedDict[o][0] == min_1:
                uzi_izbor.update({o:orderedDict[o]})
    
        orderedDict = collections.OrderedDict(sorted(uzi_izbor.iteritems(), key=lambda (k,v):v[1]))       
#        print("sortirano 2")
#        for o in orderedDict:
#            print orderedDict[o]
        #iz nekog razloga nece vratiti uredeni par {key, value} pa sam ovako napravio
        mergeEdge = dict()
        mergeEdge[orderedDict.keys()[0]] = orderedDict.values()[0]
        return mergeEdge

    '''
        usporedujemo weightove cvora koji na kojemu se izvrsava i onog koji je poslao poruku
        Ako je weight cvora manji onda ostavljamo kako je bilo, ako nije onda mijenjamo weigthove
        u trenutnom cvoru. S obzirom da zelimo imati putanju poruka kako ne bi morali raditi broadcast
        od roota prema mergeEdgu, memory    oramo promijeniti nas dicitonary koji je bio <id cvora koji je poslao poruku 
        onom koji je poslao poruku trenutnom: mergeEdge Weight> u {id cvora koji je poslao poruku: mergeEgde Weight}.
        Mijenjamo samo vlasnika mergeEdge Weighta kako bi znali put od roota prema istome. Weight ostaje isti.  
    '''
    def min_weight_two_nods(self, node_id_weight_a, message_source, node):
        # node_id_* je dictionary <id  cvora koji je poslao poruku: weight>
        # NIKAD NE ZABORAVI KREIRAT NOVU VARIAJABlU SA KONTSTRUKTOROM ISTE AKO CES JOJ DODIJELTII VEC
        # POTOSTOJECE VRIJEDNOSTI ....
        node_id_weight_b = dict(message_source.memory[self.nodeEdgeKey])
        weight_node_a = node_id_weight_a.values()
        weight_node_b = node_id_weight_b.values()
        #node.memory[self.debugKey] = [node_id_weight_a, node_id_weight_b]

        if weight_node_a[0]<weight_node_b[0]:
            node.memory[self.nodeEdgeKey] = node_id_weight_a
            return
        elif weight_node_a>weight_node_b[0]:
            temp = dict()
            temp[message_source] =  node_id_weight_b.pop(node_id_weight_b.keys()[0])
            #node_id_weight_b[message_source] = node_id_weight_b.pop(node_id_weight_b.keys()[0])
            #return node_id_weight_b
            node.memory[self.nodeEdgeKey] = temp
            return
        elif weight_node_a[1]<weight_node_b[1]:
            node.memory[self.nodeEdgeKey] = node_id_weight_a
            return
        else:
            temp = dict()
            temp[message_sourc] = node_id_weight_b.pop(node_id_weight_b.keys()[0])
            #node_id_weight_b[message_source] = node_id_weight_b.pop(node_id_weight_b.keys()[0])
            #return node_id_weight_b
            node.memory[self.nodeEdgeKey] = temp
            return

    def min_id_two_nodes(self, node1, node2):
        if node1.id < node2.id:
            return node1
        else:
            return node2

    STATUS = {
              'AVAILABLE': available,
              'PROCESSING': processing,
              'SATURATED': saturated,
             }

#   sam sebi je merge edge - node posalje parentu da je gotovo, a nije jer mu vi linkovi nisu internal
#   kako onda birati egde? ako nema unuseda, onda queue. rpoblem je ako ostane jedan cvor na kraju mreze sta onda?

#   s boziro mda imam omerge link absorb ne bi trebao voditi ka merge linku ako smo vec  poslali report parentu. to moramo rjesit. djelomicno
#   povecaj report counter pri prvom slanju late, a drugi mcvorovima digni late u primanju i zabrani send_outside