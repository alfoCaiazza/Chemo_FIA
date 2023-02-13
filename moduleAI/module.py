import random
import json

# Il modulo prende in input i pazienti sottomessi dal medico: per far comunicare Java e Python
# utilizziamo un file condiviso tra i due linguaggi: Java scrive l'input, preso da Python, e Python
# scrive l'output preso da Java per visualizzare lo schedule

file = open('patients.json', 'r')
patients = json.loads(file.read())
print("Patients number: " + str(len(patients)))

file = open('medicines.json', 'r')
medicines = json.loads(file.read())


def encodeIndividual(patientList, numSeats, numHours, numDays):
    column = len(patientList)
    row = numSeats * numHours * numDays
    matrix = []

    if column < row or column == row:
        for i in range(column):
            for j in range(row):
                lista = random.sample([0, 1], counts=[column - 1, 1], k=column)

            matrix.append(lista)
        return matrix
    elif column > row:  # o si impone un limite al form o si eliminano pazienti a random
        print("Selezionare un numero di pazienti ridotto: inferiore alle X unita")


def generation(patients, numSeats, numHours, numDays):
    population_size = 1000
    population = []
    newIndividual = []
    for i in range(population_size):
        newIndividual = encodeIndividual(patients, numSeats, numHours, numDays)
        population.append(newIndividual)
        newIndividual = []
    return population


def fitness(generation, patients):
    values = []
    conflict = 0
    for indi in generation:
        fit_of_indi = 0
        lista_indici_pazienti = indexPatients(indi)

        for i in range(len(patients)):
            for j in range(len(patients) - 1):
                for k in range(len(patients) - 2):
                    fit = 0
                    if j == i + 1 and k == j + 1:
                        if patients[lista_indici_pazienti[i]]['medicineId'] == patients[lista_indici_pazienti[j]][
                            'medicineId'] and patients[lista_indici_pazienti[j]]['medicineId'] == \
                                patients[lista_indici_pazienti[k]]['medicineId']:
                            fit += 0.7
                        elif patients[lista_indici_pazienti[i]]['medicineId'] == patients[lista_indici_pazienti[j]][
                            'medicineId']:
                            fit += 0.3
                    fit_of_indi += fit

        for i in range(len(medicines)):
            val = 0
            quantity = medConsume(medicines[i], patients, medicines[i]['quantity'])
            if quantity < 0:
                val += 0.3
            elif quantity < (medicines[i]['quantity'] * 0.5):
                val += 0.1
            fit_of_indi += val

        values.append(fit_of_indi)

    return values


def medConsume(medicine, patients, totQuant):
    for pat in patients:
        if pat['medicineId'] == medicine['medicineId']:
            totQuant -= pat['dose']
    return totQuant


# La prima generazione di soluzioni, generate in modo casaule, è pessima: non esistono schedulazioni che considerano tutti gli individui
def countConflict(schedule):
    lista_indici_pazienti = indexPatients(schedule)
    res = []
    conflict = False
    for elem in lista_indici_pazienti:
        if elem not in res:
            res.append(elem)
        else:
            conflict = True

    print(len(res), res)
    return conflict


def indexPatients(schedule):
    lista = []
    for elem in schedule:
        index = elem.index(1)
        lista.append(index)
    return lista


def crossover(ind1, ind2, numPatients):
    newIndi = []
    values = []
    val = [0, 1]
    prob = [.2, .8]
    probCrossover = random.choices(val, prob)

    if probCrossover[0] == 1:
        for el in range(int(len(ind1) / 2)):
            if ind1[el].index(1) not in values:
                values.append(ind1[el].index(1))
                newIndi.append(ind1[el])

        for el in range(len(ind2)):
            if len(newIndi) < numPatients:
                if ind2[el].index(1) not in values:
                    values.append(ind2[el].index(1))
                    newIndi.append(ind2[el])

        if len(newIndi) < numPatients:
            for i in range(numPatients):
                default_indi = [0] * numPatients
                if i not in values:
                    default_indi[i] = 1
                    newIndi.append(default_indi)

    return newIndi


def rouletteWheel(fitness):
    winners = []
    pos = 0
    i = 0
    probabilities = []
    total_fitness = sum(fitness)  # calcolo del valore di fitness totale

    for value in fitness:
        probabilities.append({"position": pos,
                              "probability": value / total_fitness})  # viene creato un array dove vengono memorizzate le probabilità e gli indici di esse (questi corrispondono agli indici che gli individui hanno nell'array popolazione)
        pos += 1

    while i < len(fitness):  # il ciclo viene iterato tante volte quanti sono gli individui della popolazione
        win = random.choice(probabilities)  # viene estratto il vincitore
        #se il vincitore non è gia presente tra quelli precedentemente estratti viene aggiunto all'array
        winners.append(win.get("position"))
        i += 1
    return winners


def mutation(individual):
    val = [0, 1]
    prob = [.99, .01]
    probMutation = random.choices(val, prob)
    if probMutation[0] == 1:
        nraw = len(patients) - 1
        row1 = random.randint(0, nraw)
        row2 = random.randint(0, nraw)
        temp = individual[row1]
        individual[row1] = individual[row2]
        individual[row2] = temp
        return individual
    else:
        return individual


def algorithm():
    population = generation(patients, 5, 5, 5)
    populationSize = len(population)
    max_fit = 0

    #forse è meglio aggiungere un certo numero di possibilità da dare all'algoritmo
    while populationSize > 0:
        fit = fitness(population, patients)
        max_next = max(fit)
        chance = 2 #Diamo all'algoritmo due possbilità per continuare a cercare una soluzione migliore nel caso in cui quella attuale sia peggiore della precedente

        if max_next < max_fit:
            chance -= 1
            if chance == 0:
                return best
        else:
            best = population[fit.index(max_next)]
            max_fit = max_next

        selectedIndividuals = rouletteWheel(fit)

        if len(selectedIndividuals) <= 2:
            return best

        nextGen = []
        for i in range(len(selectedIndividuals)):
            for j in range(len(selectedIndividuals)):
                if j == i + 1:
                    newIndi = crossover(population[selectedIndividuals[i]], population[selectedIndividuals[j]],
                                        len(patients))
                    if newIndi:
                        newIndi = mutation(newIndi)
                        nextGen.append(newIndi)
        population = nextGen
        populationSize = len(population)
        print(populationSize)


def printSchedule(schedule):
    for i in range(len(patients)):
        if i <= 4:
            if i == 0:
                print("LUNEDI ore 9:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname'] + ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 4 < i <= 9:
            if i == 6:
                print("LUNEDI ore 10:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 9 < i <= 14:
            if i == 11:
                print("LUNEDI ore 11:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 14 < i <= 19:
            if i == 16:
                print("LUNEDI ore 12:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 19 < i <= 24:
            if i == 21:
                print("MARTEDI ore 9:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 24 < i <= 29:
            if i == 26:
                print("MARTEDI ore 10:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 29 < i <= 34:
            if i == 31:
                print("MARTEDI ore 11:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 34 < i <= 39:
            if i == 36:
                print("MARTEDI ore 12:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 39 < i <= 44:
            if i == 41:
                print("MERCOLEDI ore 9:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 44 < i <= 49:
            if i == 46:
                print("MERCOLEDI ore 10:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 49 < i <= 54:
            if i == 51:
                print("MERCOLEDI ore 11:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 54 < i <= 59:
            if i == 56:
                print("MERCOLEDI ore 12:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 59 < i <= 64:
            if i == 61:
                print("GIOVEDI ore 9:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 64 < i <= 69:
            if i == 66:
                print("GIOVEDI ore 10:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 69 < i <= 74:
            if i == 71:
                print("GIOVEDI ore 11:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 74 < i <= 79:
            if i == 76:
                print("GIOVEDI ore 12:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 79 < i <= 84:
            if i == 81:
                print("VENERDI ore 9:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 84 < i <= 89:
            if i == 86:
                print("VENERDI ore 10:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 89 < i <= 94:
            if i == 91:
                print("VENERDI ore 11:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))
        elif 94 < i <= 99:
            if i == 96:
                print("VENERDI ore 12:00:")
            print("\t" + patients[schedule[i].index(1)]['name'] + " " + patients[schedule[i].index(1)]['surname']+ ": " + str(patients[schedule[i].index(1)]['medicineId']))


population = algorithm()
printSchedule(population)
