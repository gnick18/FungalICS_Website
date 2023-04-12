from dna_features_viewer import GraphicFeature, GraphicRecord
import bokeh
from bokeh.plotting import figure, output_file, save, show
from bokeh.io import output_notebook
import matplotlib.pyplot as plt
import matplotlib.font_manager
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import pandas as pd
import os
import pdb
from bokeh.embed import file_html
from bokeh.resources import CDN
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from Bio import SeqIO

#changing the default font
import matplotlib
matplotlib.rcParams['font.family'] = "Arial"

#global variables
domains = r'./Data/SupTable4.tsv'
domainsDF = pd.read_csv(domains, sep='\t')

#subfunction that defines the color of the gene arrows
def GetColor(domains):
    colorDictionary = {"MultiDomain": "#F94144",
    "ICS": "#90BE6D",
    "MFS": "#F3722C",
    "p450": "#F8961E",
    "Isocyanide hydratase": "#43AA8B",
    "No domain": "#577590",
    "Other": "#F9C74F"}

    #Rules, if there is an ICS, always color that color. Otherwise if it's multidomain, default to that 
    #no domain
    if str(domains[0]) == 'nan':
        return colorDictionary["No domain"]
    #ics
    if "DIT1_PvcA" in domains:
        return colorDictionary["ICS"]
    #multidomain
    if len(domains) > 1:
        return colorDictionary['MultiDomain']
    #other specified domains
    if "MFS" in domains:
        return colorDictionary['MFS']
    elif "p450" in domains:
        return colorDictionary['p450']
    elif "DJ-1_PfpI" in domains:
        return colorDictionary["Isocyanide hydratase"]
    else:
        return colorDictionary['Other']


#subfunction to get the names and proteins
def CreateGeneMapping(gffDF, bgcName):
    bgcMapping = {}
    genesOnly = gffDF[gffDF['featureType'] == "gene"]
    for index, row in genesOnly.iterrows():
        #gathering all of the information
        geneStart = row['start']
        geneStop = row['stop']
        geneName = row['info'].split(";")[0].split("gene-")[-1]
        if "gene" in geneName:
            geneName = geneName.split("ene")[-1]
        direction = row['dir']
        cdsRegions = gffDF[(gffDF['info'].str.contains(geneName)) & (gffDF['featureType'] == "CDS")]
        if len(cdsRegions) == 0:
            continue
            # #this means you need to get the protein name from the exon
            # exons = gffDF[(gffDF['info'].str.contains(geneName)) & (gffDF['featureType'] == "mRNA")]
            # topCDS_info = exons.iloc[0,8]
            # proteinName = topCDS_info.split(";")[0].split("rna-")[-1]
        else:
            topCDS_info = cdsRegions.iloc[0,8]
            proteinName = topCDS_info.split("protein_id=")[-1]
        if ";" in proteinName:
            proteinName = proteinName.split(";")[0]
        #getting the domains in this protein
        domainsInProtein = domainsDF[domainsDF['Protein'] == proteinName]
        if len(domainsInProtein) == 0:
            pdb.set_trace()
        domains = domainsInProtein['Domain'].unique().tolist()
        color = GetColor(domains)

        #adding this to the mapping dictionary
        bgcMapping[geneName] = {"start": geneStart,"stop":geneStop,"proteinName":proteinName,"domains":domains, "dir":direction, "color": color}
    #returning the results
    return bgcMapping


#main function to creat the gffDF visualization
def CreateBGC_Vis(gffDF, bgcSequence, bgcName, clusterPath):
    bgcMapping = CreateGeneMapping(gffDF, bgcName)
    features = []
    for gene in bgcMapping:
        geneMap = bgcMapping[gene]
        #loading all of the data from the mapping file
        start = geneMap['start']
        stop = geneMap['stop']
        protName = geneMap['proteinName']
        direction_str = geneMap["dir"]
        geneColor = geneMap["color"]
        if direction_str == "+":
            direction = +1
        else:
            direction = -1
        #need this conditional in case their are no domains in the list
        if str(geneMap['domains'][0]) == 'nan':
            domains = "nan"
        else:
            domains = ", ".join(geneMap['domains'])

        htmlText = protName + ": " + domains
        features.append(GraphicFeature(start=start, end=stop,
                                        strand=direction, color=geneColor,
                                          html=htmlText, label=gene,
                                          thickness=20))
    #making the record object
    seqLength = len(bgcSequence)
    record = GraphicRecord(sequence=bgcSequence, features=features)
    try:
        plot = record.plot_with_bokeh(figure_width=10, figure_height="auto")
    except:
        print(bgcName + " broke")
        return
    #saving this as an html file
    htmlOutput = os.path.join(clusterPath, bgcName + ".html")
    html = file_html(plot, CDN, title=bgcName)
    with open(htmlOutput, "w") as out:
        out.write(html)



#the wrapper function that loops over all the data
def LoopOverBGCs(rootDir):
    counter = 0
    for accession in os.listdir(rootDir):
        accPath = os.path.join(rootDir, accession)
        if accession.startswith("."):
            continue
        for cluster in os.listdir(accPath):
            clusterPath = os.path.join(accPath, cluster)
            if os.path.isdir(clusterPath) and cluster.startswith("Cluster"):
                #getting the name and file location, this will get passed onto the visualizer program
                bgcName = ""
                gffFile = ""
                for bgcFile in os.listdir(clusterPath):
                    if not bgcFile.startswith("."):
                        if bgcFile.endswith(".gff"):
                            gffFile = os.path.join(clusterPath, bgcFile)
                        elif bgcFile.endswith(".gbk"):
                            bgcName = bgcFile.split(".gb")[0]
                        elif bgcFile.endswith(".fna"):
                            # Open the FASTA file and read the first sequence
                            fnaPath = os.path.join(clusterPath, bgcFile)
                            record = next(SeqIO.parse(fnaPath , "fasta"))
                            # Extract the sequence as a string
                            bgcSequence = str(record.seq)

                #running the visualiztion program
                gffDF = pd.read_csv(gffFile, sep='\t', names = ['contig','source','featureType','start','stop','n1','dir','n2','info'])
                CreateBGC_Vis(gffDF, bgcSequence, bgcName, clusterPath)
                counter += 1
                if counter % 10 == 0:
                    print("Finished " + str(counter))


#the main
if __name__ == '__main__':
    rootDir = r'/Users/gnickles/Desktop/FungalICS_Website/Data/ICSBGCs'
    LoopOverBGCs(rootDir)

