import threading

NUM_DOCTORS = 5


class Screwdriver:
    def __init__(self):
        self.lock = threading.Lock()

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()


class Doctor:
    def __init__(self, id, left_screwdriver, right_screwdriver, start_barrier):
        self.id = id
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver
        self.start_barrier = start_barrier

    def operate(self):
        self.start_barrier.wait()
        self.left_screwdriver.acquire()
        self.right_screwdriver.acquire()
        print(f"Doctor {self.id}: BLAST!")

        # Задержка в потоке на 1 секунду
        delay_event = threading.Event()
        delay_event.wait(0.01)

        self.right_screwdriver.release()
        self.left_screwdriver.release()


def doctors_initialize():
    screwdriver = [Screwdriver() for _ in range(NUM_DOCTORS)]
    doctors = []

    start_barrier = threading.Barrier(NUM_DOCTORS)

    for i in range(NUM_DOCTORS):
        left_screw = screwdriver[i]

        if i < NUM_DOCTORS - 1:
            right_screw = screwdriver[i + 1]
        else:
            right_screw = screwdriver[0]

        doctor = Doctor(i + 9, left_screw, right_screw, start_barrier)
        doctors.append(doctor)

    return doctors, start_barrier


def action(doctors, start_barrier):
    threads = []
    for doctor in doctors:
        thread = threading.Thread(target=doctor.operate)
        thread.start()
        threads.append(thread)

    start_barrier.reset()  # Сбрасываем барьер старта

    for thread in threads:
        thread.join()


def main():
    doctors, start_barrier = doctors_initialize()
    action(doctors, start_barrier)


if __name__ == "__main__":
    main()
