# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo: Carlos Augusto Littig
#    Matrícula: 202203793    
#    Turma: CC5N
#    Email: carlosaugusto98p@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage

# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        if x < 0:
            x = 0  
        elif x >= self.largura:
            x = self.largura - 1  # Use o valor da última coluna

        if y < 0:
            y = 0  
        elif y >= self.altura:
            y = self.altura - 1  

        # Cálculo do índice a partir das coordenadas ajustadas
        index = y * self.largura + x
        return self.pixels[index]


    def set_pixel(self, x, y, c):

        #set corrigido para pegar valores de um array
        index = y * self.largura + x
        self.pixels[index] = c

    def aplicar_por_pixel(self, func):

        # aplica um valor em cada pixel

        resultado = Imagem.nova(self.largura, self.altura)
        for y in range(self.altura):
            for x in range(self.largura):
                cor = self.get_pixel(x, y)
                nova_cor = func(cor)
                resultado.set_pixel(x, y, nova_cor)
        return resultado


    def aplicarKernel(self, kernel):
        '''
        Explicação da função: Aplica um kernel na imagem chamando a função
                            aplicar por pixel.

        input: self
        output: Imagem
        '''
        tamanho_kernel = kernel[0]
        kernel_dados = kernel[2]

        imagem_altura = self.altura
        imagem_largura = self.largura

        if len(kernel_dados) != tamanho_kernel * tamanho_kernel:
            raise Exception("Kernel inválido")

        nova_imagem = Imagem.nova(imagem_largura, imagem_altura)

        offset = tamanho_kernel // 2

        for y in range(imagem_altura):
            for x in range(imagem_largura):
                soma = 0.0  

                for ky in range(-offset, offset + 1):
                    for kx in range(-offset, offset + 1):
                        pixel_x = x + kx
                        pixel_y = y + ky

                        valor_pixel = self.get_pixel(pixel_x, pixel_y)
                        valor_kernel = kernel_dados[(ky + offset) * tamanho_kernel + (kx + offset)]
                        soma += valor_pixel * valor_kernel

                nova_imagem.set_pixel(x, y, min(max(int(round(soma)), 0), 255))

        return nova_imagem

    
    def subImagem(self, subtraendo):
        '''
        Explicação da função: subtrai duas imagens

        input: self, subtraendo
        output: Imagem
        '''
        if self.altura != subtraendo.altura or self.largura != subtraendo.largura:
            raise Exception("imagens de tamanhos diferentes")
        
        resultado = Imagem.nova(self.largura, self.altura)

        for x in range(self.largura):
            for y in range(self.altura):
                valor = round(self.get_pixel(x,y) - subtraendo.get_pixel(x,y))
                if(valor < 0):
                    valor = 0
                elif(valor > 255):
                    valor = 255
                
                resultado.set_pixel(x,y, valor)

        return resultado

    def mulImgEscalar( self, escalar):

        '''
        Explicação da função: mulitplica uma imagem por um escalar

        input: self, escalar
        output: Imagem
        '''

        resultado = Imagem.nova(self.largura, self.altura)

        for y in range(self.altura):
            for x in range(self.largura):
                valor = self.get_pixel(x,y) * escalar
                resultado.set_pixel(x,y, valor)

        resultado.salvar("./test_images/mulImgEscalar.png")
        return resultado


    def invertida(self):
      '''
      Explicação da função: Inverte os tons da imagem chamando a função
                            aplicar por pixel, é passada uma função lambda
                            que subtrai o valor da cor do pixel de 255, que é o 
                            valor maximo que o pixel pode ter.
      
      input: self
      output: Imagem
      '''     
      return self.aplicar_por_pixel(lambda c: 255 - c)
       
    def borrada(self, n):

        '''
        Explicação da função: calcula e aplica um kernel na imagem ppara deixa-la borradapodendo ficar mais borrada dependendo do valor de n

        input: self, n
        output: Imagem
        '''

        
        valor = 1/(n*n)
        kernel =[n,n,[valor] * (n*n)]
        
        
        resultado = self.aplicarKernel(kernel)

        for y in range(resultado.altura):
            for x in range(resultado.largura):
                valor = resultado.get_pixel(x, y)
                if(valor < 0):
                    valor = 0
                elif (valor > 255):
                    valor = 255

                valor_arredondado = int(round(valor))
                resultado.set_pixel(x, y, valor_arredondado)

        return resultado

    def focada(self, n):
        '''
        Explicação da função: borra a imagem, em seguida, pega a original e multiplica por dois e por ultimo a subtrai da borrada

        input: self, n
        output: Imagem
        '''
        borrada = self.borrada(n)

        selfMultiplicada = self.mulImgEscalar(2)

        resultado = selfMultiplicada.subImagem(borrada)
        

        return resultado

    def bordas(self):
        
        '''
            Explicação da função: calcula as bordas da imagem usando o operador Sobel.

            A função aplica o operador Sobel, usando duas matrizes de convolução (kernels) para detectar bordas nos eixos horizontal (X) e 
            vertical (Y), identificando contornos na imagem onde há mudanças significativas de brilho.


        input: self
        output: Imagem
        '''

        resultado = Imagem.nova(self.largura, self.altura)

        kernelX = [3,3,[ -1,0,1
                         ,-2,0,2
                         ,-1,0,1]]
        
        kernelY = [3,3,[ -1,-2,-1
                          ,0,0,0
                          ,1,2,1]]


        imagemX = Imagem.nova(self.largura, self.altura)
        imagemY = Imagem.nova(self.largura, self.altura)

        tamanhoKernel = kernelX[0]

        kernel_dadosX = kernelX[2]
        kernel_dadosY  = kernelY[2]

        imagem_altura = self.altura 
        imagem_largura = self.largura
        offset = tamanhoKernel // 2

        for y in range(imagem_altura):
            for x in range(imagem_largura):
                soma = 0.0

                for ky  in range(-offset, offset+1):
                    for kx in range(-offset, offset+1):
                        pixel_x = x + kx
                        pixel_y = y + ky

                        valor_pixel = self.get_pixel(pixel_x, pixel_y)
                        valor_kernel = kernel_dadosX[(ky + offset) * tamanhoKernel + (kx + offset)]
                        soma += valor_pixel * valor_kernel

                imagemX.set_pixel(x, y, soma)

        for y in range(imagem_altura):
            for x in range(imagem_largura):
                soma = 0.0

                for ky  in range(-offset, offset+1):
                    for kx in range(-offset, offset+1):
                        pixel_x = x + kx
                        pixel_y = y + ky

                        valor_pixel = self.get_pixel(pixel_x, pixel_y)
                        valor_kernel = kernel_dadosY[(ky + offset) * tamanhoKernel + (kx + offset)]
                        soma += valor_pixel * valor_kernel

                imagemY.set_pixel(x, y, soma)

        for y in range(self.altura):
            for x in range(self.largura):
                valorX = (imagemX.get_pixel(x,y)) **2
                valorY = (imagemY.get_pixel(x,y)) **2

                valor = int(round((valorX + valorY) ** 0.5))

                if(valor < 0):
                    valor = 0
                elif(valor > 255):
                    valor = 255
                
                resultado.set_pixel(x,y, valor)

        return resultado
    

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    pass

    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
 

    #questão dois
    img = Imagem.carregar("./test_images/bluegill.png")
    img = img.invertida()    
    img.salvar("./test_results/bluegillResultadoQ2.png")
    

    #questão quatro

    kernel = [9, 9, [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0
    ]]

    img4 = Imagem.carregar("./test_images/pigbird.png")
    img4 = img4.aplicarKernel(kernel)
    img4.salvar("./test_results/pigbirdResultadoQ4.png")

    

    