# PyLiPD
Python LiPD utilities

## Installation
    pip install pylipd

## Usage

### Loading local LiPD files
    from pylipd.lipd import LiPD
    lipd = LiPD()
    lipd.load(["MD98_2181.Stott.2007.lpd", "Ant-WAIS-Divide.Severinghaus.2012.lpd", "Asi-TDAXJP.PAGES2k.2013.lpd"])

### Loading LiPD data from GraphDB server
    from pylipd.lipd import LiPD
    lipd = LiPD()
    lipd.set_endpoint("https://linkedearth.graphdb.mint.isi.edu/repositories/LiPDVerse2")
    lipd.load_remote_datasets(["MD98_2181.Stott.2007", "Ant-WAIS-Divide.Severinghaus.2012", "Asi-TDAXJP.PAGES2k.2013"])