# Auto-LoloBarrel
Auto connect texture based on a tag system in the names

To run in maya: 

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


![image](https://github.com/Krunkeat/Auto-LoloBarrel/assets/50023258/4b2d9e53-d0d7-4d6b-add3-f86a3a268f3e)
