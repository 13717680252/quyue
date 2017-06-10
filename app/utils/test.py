import json

import redis
import datetime
def loadDataSet():
    return [ [ "wc", "jb", "sb","cao" ], [ "2b", "jb", "cao" ], [  "wc","2b",  "jb","sb", "cao" ], [ "2b", "jb","sb","cao" ] ]
def createC1( dataSet ):
    '''''
        构建初始候选项集的列表，即所有候选项集只包含一个元素，
        C1是大小为1的所有候选项集的集合
    '''
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if [ item ] not in C1:
                C1.append( [ item ] )
    C1.sort()
    #return map( frozenset, C1 )
    #return [var for var in map(frozenset,C1)]
    return [frozenset(var) for var in C1]
def scanD( D, Ck, minSupport ):
    '''''
        计算Ck中的项集在数据集合D(记录或者transactions)中的支持度,
        返回满足最小支持度的项集的集合，和所有项集支持度信息的字典。
    '''
    ssCnt = {}
    for tid in D:                  # 对于每一条transaction
        for can in Ck:             # 对于每一个候选项集can，检查是否是transaction的一部分 # 即该候选can是否得到transaction的支持
            if can.issubset( tid ):
                ssCnt[ can ] = ssCnt.get( can, 0) + 1
    numItems = float( len( D ) )
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[ key ] / numItems                   # 每个项集的支持度
        if support >= minSupport:                           # 将满足最小支持度的项集，加入retList
            retList.insert( 0, key )
        supportData[ key ] = support                        # 汇总支持度数据
    return retList, supportData
def aprioriGen( Lk, k ): # Aprior算法
    '''''
        由初始候选项集的集合Lk生成新的生成候选项集，
        k表示生成的新项集中所含有的元素个数
    '''
    retList = []
    lenLk = len( Lk )
    for i in range( lenLk ):
        for j in range( i + 1, lenLk ):
            L1 = list( Lk[ i ] )[ : k - 2 ];
            L2 = list( Lk[ j ] )[ : k - 2 ];
            L1.sort();L2.sort()
            if L1 == L2:
                retList.append( Lk[ i ] | Lk[ j ] )
    return retList
def apriori( dataSet, minSupport = 0.5 ):
    C1 = createC1( dataSet )                                # 构建初始候选项集C1
    #D = map( set, dataSet )                                 # 将dataSet集合化，以满足scanD的格式要求
    #D=[var for var in map(set,dataSet)]
    D=[set(var) for var in dataSet]
    L1, suppData = scanD( D, C1, minSupport )               # 构建初始的频繁项集，即所有项集只有一个元素
    L = [ L1 ]                                              # 最初的L1中的每个项集含有一个元素，新生成的
    k = 2                                                   # 项集应该含有2个元素，所以 k=2

    while ( len( L[ k - 2 ] ) > 0 ):
        Ck = aprioriGen( L[ k - 2 ], k )
        Lk, supK = scanD( D, Ck, minSupport )
        suppData.update( supK )                             # 将新的项集的支持度数据加入原来的总支持度字典中
        L.append( Lk )                                      # 将符合最小支持度要求的项集加入L
        k += 1                                              # 新生成的项集中的元素个数应不断增加
    return L, suppData                                      # 返回所有满足条件的频繁项集的列表，和所有候选项集的支持度信息
def calcConf( freqSet, H, supportData, brl, minConf=0.7 ):  # 规则生成与评价
    '''''
        计算规则的可信度，返回满足最小可信度的规则。
        freqSet(frozenset):频繁项集
        H(frozenset):频繁项集中所有的元素
        supportData(dic):频繁项集中所有元素的支持度
        brl(tuple):满足可信度条件的关联规则
        minConf(float):最小可信度
    '''
    prunedH = []
    for conseq in H:
        conf = supportData[ freqSet ] / supportData[ freqSet - conseq ]
        if conf >= minConf:
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append( ( freqSet - conseq, conseq, conf ) )
            prunedH.append( conseq )
    return prunedH

def rulesFromConseq( freqSet, H, supportData, brl, minConf=0.7 ):
    '''''
        对频繁项集中元素超过2的项集进行合并。
        freqSet(frozenset):频繁项集
        H(frozenset):频繁项集中的所有元素，即可以出现在规则右部的元素
        supportData(dict):所有项集的支持度信息
        brl(tuple):生成的规则
    '''
    m = len( H[ 0 ] )
    if len( freqSet ) > m + 1: # 查看频繁项集是否足够大，以到于移除大小为 m的子集，否则继续生成m+1大小的频繁项集
        Hmp1 = aprioriGen( H, m + 1 )
        Hmp1 = calcConf( freqSet, Hmp1, supportData, brl, minConf ) #对于新生成的m+1大小的频繁项集，计算新生成的关联规则的右则的集合
        if len( Hmp1 ) > 1: # 如果不止一条规则满足要求（新生成的关联规则的右则的集合的大小大于1），进一步递归合并，
                            #这样做的结果就是会有“[1|多]->多”(右边只会是“多”，因为合并的本质是频繁子项集变大，
                            #而calcConf函数的关联结果的右侧就是频繁子项集）的关联结果
            rulesFromConseq( freqSet, Hmp1, supportData, brl, minConf )

def generateRules( L, supportData, minConf=0.7 ):
    '''''
        根据频繁项集和最小可信度生成规则。
        L(list):存储频繁项集
        supportData(dict):存储着所有项集（不仅仅是频繁项集）的支持度
        minConf(float):最小可信度
    '''
    bigRuleList = []
    for i in range( 1, len( L ) ):
        for freqSet in L[ i ]:                                                      # 对于每一个频繁项集的集合freqSet
            H1 = [ frozenset( [ item ] ) for item in freqSet ]
            if i > 1:# 如果频繁项集中的元素个数大于2，需要进一步合并，这样做的结果就是会有“[1|多]->多”(右边只会是“多”，
                     #因为合并的本质是频繁子项集变大，而calcConf函数的关联结果的右侧就是频繁子项集），的关联结果
                rulesFromConseq( freqSet, H1, supportData, bigRuleList, minConf )
            else:
                calcConf( freqSet, H1, supportData, bigRuleList, minConf )
    return bigRuleList


def GETData(myDat):                                  # 导入数据集
    D = [set(var) for var in myDat]
    L, suppData = apriori( myDat, 0.6 )                     # 选择频繁项集
    #print(u"频繁项集L：", L)
    print(u"所有候选项集的支持度信息：", suppData)
    ##rules = generateRules( L, suppData, minConf=0.7 )
    ##print('rules:\n', rules)
    return suppData