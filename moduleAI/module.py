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
    population_size = random.randrange(len(patients) + 1, 30)
    print("Population size: " + str(population_size))
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
                    if j == i+1 and k == j+1:
                        if patients[lista_indici_pazienti[i]]['medicineId'] == patients[lista_indici_pazienti[j]]['medicineId'] and patients[lista_indici_pazienti[j]]['medicineId'] == patients[lista_indici_pazienti[k]]['medicineId']:
                            fit += 0.7
                        elif patients[lista_indici_pazienti[i]]['medicineId'] == patients[lista_indici_pazienti[j]]['medicineId']:
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


#La prima generazione di soluzioni, generate in modo casaule, è pessima: non esistono schedulazioni che considerano tutti gli individui
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

    for elem in range(int(len(ind1)/2)):
        if ind1[elem].index(1) not in values:
            values.append(ind1[elem].index(1))
            newIndi.append(ind1[elem])

    for elem in ind2:
        if len(newIndi) < numPatients:
            if elem.index(1) not in values:
                values.append(elem.index(1))
                newIndi.append(elem)


    if len(newIndi) < numPatients:
        for i in range(numPatients):
            default_indi = [0] * numPatients
            if i not in values:
                default_indi[i] = 1
                newIndi.append(default_indi)

    return newIndi


gen = generation(patients, 6, 6, 5)
fit = fitness(gen, patients)
print(fit)