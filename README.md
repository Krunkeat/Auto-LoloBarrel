# Auto-LoloBarrel
Auto connect texture based on a tag system in the names

To run in maya : 
    import Auto_LoloBarrel_v02
    import importlib

    importlib.reload(Auto_LoloBarrel_v02)


    if __name__ == "__main__":
        try:
            ui2.deleteLater()
        except:
            pass
        ui2 = Auto_LoloBarrel_v02.Auto_LoloBarrelUI()

        try:
            ui2.show()
        except:
            ui2.deleteLater()


