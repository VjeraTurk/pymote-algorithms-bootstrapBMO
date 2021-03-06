

def prepare_absorption(self):
        node = self.network.nodes()[0]
        node.memory[self.levelKey] = 4
        node.memory[self.numberOfInternalNodesKey] = 3
        #for (k,v in node.memory[self.linkStatusKey])
        node2 = self.network.nodes()[1]
        node2.memory[self.levelKey] = 4
        node2.memory[self.numberOfInternalNodesKey] = 1
        node6 = self.network.nodes()[5]
        node6.memory[self.levelKey] = 4
        node6.memory[self.numberOfInternalNodesKey] = 2
        node4 = self.network.nodes()[3]
        node4.memory[self.levelKey] = 4
        node4.memory[self.numberOfInternalNodesKey] = 1
        node2.memory[self.parentKey] = node
        node6.memory[self.parentKey] = node4
        node.memory[self.parentKey] = node6
        node2.memory[self.nameKey] = node4.memory[self.nameKey]
        node6.memory[self.nameKey] = node4.memory[self.nameKey]
        node.memory[self.nameKey] = node4.memory[self.nameKey]
        node.memory[self.linkStatusKey][node2] = 'INTERNAL'
        node.memory[self.linkStatusKey][node6] = 'INTERNAL'
        node2.memory[self.linkStatusKey][node] = 'INETRNAL'
        node6.memory[self.linkStatusKey][node] = 'INTERNAL'
        node6.memory[self.linkStatusKey][node4] = 'INTERNAL'
        node4.memory[self.linkStatusKey][node6] = 'INTERNAL'
        node3 = self.network.nodes()[2]
        node3.memory[self.levelKey] = 4
        node7 = self.network.nodes()[6]
        node7.memory[self.levelKey] = 6
        node3.memory[self.nameKey] = node4.memory[self.nameKey]
        node3.memory[self.linkStatusKey][node] = 'INTERNAL'
        node.memory[self.linkStatusKey][node3] = 'INTERNAL'
        node3.memory[self.parentKey] = node
        node.memory[self.reportCounterKey] = 1
        node2.status = 'PROCESSING'
        node6.status = 'PROCESSING'
        node4.status = 'PROCESSING'
        node.status = 'PROCESSING'

def prepare_friendly_merger(self):
        node = self.network.nodes()[0]
        node.memory[self.levelKey] = 4
        node.memory[self.numberOfInternalNodesKey] = 3
        #for (k,v in node.memory[self.linkStatusKey])
        node2 = self.network.nodes()[1]
        node2.memory[self.levelKey] = 4
        node2.memory[self.numberOfInternalNodesKey] = 1
        node6 = self.network.nodes()[5]
        node6.memory[self.levelKey] = 4
        node6.memory[self.numberOfInternalNodesKey] = 2
        node4 = self.network.nodes()[3]
        node4.memory[self.levelKey] = 4
        node4.memory[self.numberOfInternalNodesKey] = 1
        node2.memory[self.parentKey] = node
        node6.memory[self.parentKey] = node4
        node.memory[self.parentKey] = node6
        node2.memory[self.nameKey] = node4.memory[self.nameKey]
        node6.memory[self.nameKey] = node4.memory[self.nameKey]
        node.memory[self.nameKey] = node4.memory[self.nameKey]
        node.memory[self.linkStatusKey][node2] = 'INTERNAL'
        node.memory[self.linkStatusKey][node6] = 'INTERNAL'
        node2.memory[self.linkStatusKey][node] = 'INETRNAL'
        node6.memory[self.linkStatusKey][node] = 'INTERNAL'
        node6.memory[self.linkStatusKey][node4] = 'INTERNAL'
        node4.memory[self.linkStatusKey][node6] = 'INTERNAL'
        node3 = self.network.nodes()[2]
        node3.memory[self.levelKey] = 4
        node7 = self.network.nodes()[6]
        node7.memory[self.levelKey] = 4
        #node7.memory[self.Let_us_merge_FriendlyMergerKey] = True
        #node7.memory[self.nodeEdgeKey] = {node3: [3,7]}
        #node7.memory[self.linkStatusKey][node3] = 'EXTERNAL'
        node3.memory[self.nameKey] = node4.memory[self.nameKey]
        node3.memory[self.linkStatusKey][node] = 'INTERNAL'
        node3.memory[self.numberOfInternalNodesKey] = 1
        node.memory[self.linkStatusKey][node3] = 'INTERNAL'
        node3.memory[self.parentKey] = node
        node.memory[self.reportCounterKey] = 1
        node2.status = 'PROCESSING'
        node6.status = 'PROCESSING'
        node4.status = 'PROCESSING'
        node.status = 'PROCESSING'
        try_more(self)

def try_more(self):
        node5 = self.network.nodes()[4]
        node5.memory[self.levelKey] = 7

'''node = self.network.nodes()[0]
node.memory[self.levelKey] = 3
node2 = self.network.nodes()[1]
node2.memory[self.levelKey] = 1
node2.memory[self.numberOfInternalNodesKey] = 1
node4 = self.network.nodes()[3]
node4.memory[self.levelKey] = 1
node4.memory[self.parentKey] = node2
node4.memory[self.nameKey] = node2.memory[self.nameKey]
node4.memory[self.numberOfInternalNodesKey] = 1
node4.memory[self.linkStatusKey][node2] = 'INTERNAL'
node2.memory[self.linkStatusKey][node4] = 'INTERNAL'
node4.status = 'PROCESSING'''