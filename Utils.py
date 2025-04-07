from statistics import mean


class Utils:
    @staticmethod
    def loss_function(cube: list):
        """

        :param cube:

        [0,1,2,
        3,4,5
        6,7,8]

        0+3+6 = 1+4+7 = 2+5+8 = 0+1+2 = 3+4+5 = 6+7+8

        :return:
        """
        results = [cube[0]+cube[3]+cube[6],
                   cube[1]+cube[4]+cube[7],
                   cube[2]+cube[5]+cube[6],
                   cube[0]+cube[1]+cube[3],
                   cube[3]+cube[4]+cube[5],
                   cube[6]+cube[7]+cube[8]]

        mean_sum = mean(results)

        loss = 0
        for result in results:
            if (result-mean_sum) > 0:
                loss += result-mean_sum
            else:
                loss -= result-mean_sum

        return loss
